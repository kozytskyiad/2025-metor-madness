import numpy as np
from typing import List
import plotly.io as pio
import plotly.graph_objects as go
from flask import Flask, render_template
from PIL import Image

from nbody import Body, Simulation, nbody_sim
from skybox import skybox, bg_layout, float_layout
from animation import init_frame, gen_frames

app = Flask(__name__)

@app.route('/')
def main():
	texture_file = 'starfield-small.jpg'
	positions = np.array([[0,0,0],[1,0,0]], dtype=np.float64)
	velocities = np.array([[0,0,0],[0,1.5,0.1]], dtype=np.float64)
	masses = np.array([20,1], dtype=np.float64)

	bodies: List[Body] = []
	for idx, (pos, vel, m) in enumerate(zip(positions, velocities, masses)):
		bodies.append(Body(
			position=pos,
			velocity=vel,
			rotation=0,
			mass=m,
			radius=1.0,
			name='Foo' + str(idx)
		))

	param: Simulation = Simulation(G=0.6, dt=0.5)
	snapshots: List[List[Body]] = nbody_sim(bodies, 50, param)

	# Plotting

	bg_fig = go.Figure()
	
	init_frame(bg_fig, bodies)

	frames = gen_frames(bodies, snapshots)

	skybox(bg_fig, texture_file)
	bg_fig.update_layout(bg_layout)
	bg_fig.update(frames=frames)

	bg_div = bg_fig.to_html(
		full_html=False,
		include_plotlyjs='cdn',
		auto_play=False
	)

	earth_img = Image.open('world.topo.bathy.jpg')
	nw = 500
	nh = int(nw / earth_img.width * earth_img.height)
	earth_img = earth_img.resize((nw, nh), Image.LANCZOS)

	float_fig = go.Figure(go.Image(z=earth_img))
	float_fig.update_layout(float_layout)

	float_div = float_fig.to_html(full_html=False, include_plotlyjs=False)

	return render_template(
		'index.html',
		background_plot=bg_div,
		floating_plot=float_div
	)

if __name__=='__main__':
	app.run(debug=True)
