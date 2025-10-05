import numpy as np
from typing import List
import plotly.io as pio
import plotly.graph_objects as go

from nbody import Body, Simulation, nbody_sim
from skybox import skybox

def main():
	texture_file = 'starfield-small.jpg'
	positions = np.array([[0,0,0],[1,0,0]], dtype=np.float64)
	velocities = np.array([[0,0,0],[0,2,0]], dtype=np.float64)
	masses = np.array([10,1], dtype=np.float64)

	bodies: List[Body] = []
	for idx, (pos, vel, m) in enumerate(zip(positions, velocities, masses)):
		bodies.append(Body(
			position=pos,
			velocity=vel,
			mass=m,
			radius=1.0,
			name='Foo' + str(idx)
		))

	param: Simulation = Simulation(G=0.6, dt=0.5)
	snapshots: List[List[Body]] = nbody_sim(bodies, 50, param)

	# Plotting

	fig = go.Figure()
	
	for idx, body in enumerate(bodies):
		fig.add_trace(go.Scatter3d(
			x=[body.position[0]], y=[body.position[1]], z=[body.position[2]],
			mode='markers',
			marker=dict(size=6),
			name=body.name,
			hovertemplate=f'<b>Body: {body.name}</b>'
		))
		fig.add_trace(go.Scatter3d(
			x=[], y=[], z=[],
			mode='lines',
			line=dict(width=3),
			showlegend=False,
			customdata=[idx],
			hovertemplate='<extra></extra>'
		))

	frames = []

	full_paths = [[] for _ in bodies]
	for s in snapshots:
		for idx, body in enumerate(s):
			full_paths[idx].append(body.position)

	for i, s in enumerate(snapshots):
		frame_data = []

		for j, body in enumerate(s):
			frame_data.append(go.Scatter3d(
				x=[body.position[0]],
				y=[body.position[1]],
				z=[body.position[2]],
				mode='markers',
				marker=dict(size=6),
				name=bodies[j].name
			))

			path_x = [pos[0] for pos in full_paths[j][:i+1]]
			path_y = [pos[1] for pos in full_paths[j][:i+1]]
			path_z = [pos[2] for pos in full_paths[j][:i+1]]

			frame_data.append(go.Scatter3d(
				x=path_x,
				y=path_y,
				z=path_z,
				mode='lines',
				line=dict(width=3),
				showlegend=False
			))

		frames.append(go.Frame(data=frame_data, name=f'frame{i}'))

	fig.frames = frames

	skybox(fig, texture_file)

	fig.update_layout(
		scene=dict(
			xaxis=dict(visible=False),
			yaxis=dict(visible=False),
			zaxis=dict(visible=False),
			camera=dict(eye=dict(x=0.1, y=0.1, z=0.1)),
			aspectmode='data'
		),
		margin=dict(l=0, r=0, t=0, b=0),
		paper_bgcolor='black',
		showlegend=False,
		updatemenus=[dict(
			type='buttons',
			showactive=False,
			y=1,
			x=0.8,
			xanchor='left',
			yanchor='bottom',
			buttons=[dict(
				label='Play',
				method='animate',
				args=[None, dict(
					frame=dict(duration=1, redraw=True),
					fromcurrent=True,
					transition=dict(duration=0)
				)]
			)]
		)]
	)

	fig.show()

if __name__=='__main__':
	main()
