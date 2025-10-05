import numpy as np
import plotly.io as pio
import plotly.graph_objects as go
from PIL import Image

def spherical_mesh(res_phi=180, res_theta=360):
	phi = np.linspace(0, np.pi, res_phi)
	theta = np.linspace(0, 2*np.pi, res_theta)
	phi, theta = np.meshgrid(phi, theta)

	x = np.sin(phi) * np.cos(theta)
	y = np.sin(phi) * np.sin(theta)
	z = np.cos(phi)

	return x, y, z

def load_texture(image_path, res_phi=180, res_theta=360):
	img = Image.open(image_path).convert('RGB')
	img = img.resize((res_phi, res_theta))
	img = np.array(img) / 255.0

	gray = 0.299*img[:,:,0] + 0.587*img[:,:,1] + 0.114*img[:,:,2]

	return gray

def skybox(figure, image_path, radius=100, res_phi=180, res_theta=360):
	surfacecolor = load_texture(image_path)
	x, y, z = spherical_mesh()

	x_s = radius * x
	y_s = radius * y
	z_s = radius * z

	contours = dict(
		x=dict(highlight=False),
		y=dict(highlight=False),
		z=dict(highlight=False)
	)

	figure.add_trace(go.Surface(
		x=x_s, y=y_s, z=z_s,
		surfacecolor=surfacecolor,
		colorscale='Gray',
		cmin=0, cmax=1,
		showscale=False,
		hoverinfo='skip',
		contours=contours
	))

