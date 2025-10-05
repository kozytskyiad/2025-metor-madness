import plotly.graph_objects as go
from typing import List
from nbody import Body

def init_frame(figure: go.Figure, bodies: List[Body]) -> None:
	for idx, body in enumerate(bodies):
		figure.add_trace(go.Scatter3d(
			x=[body.position[0]], y=[body.position[1]], z=[body.position[2]],
			mode='markers',
			marker=dict(size=6),
			name=body.name,
			hovertemplate=f'<b>Body: {body.name}</b>'
		))
		figure.add_trace(go.Scatter3d(
			x=[], y=[], z=[],
			mode='lines',
			line=dict(width=3),
			showlegend=False,
			customdata=[idx],
			hovertemplate='<extra></extra>'
		))

def gen_frames(init: List[Body], history: List[List[Body]]) -> List[go.Frame]:
	frames = []

	full_paths = [[] for _ in init]
	for s in history:
		for idx, body in enumerate(s):
			full_paths[idx].append(body.position)

	for i, s in enumerate(history):
		frame_data = []

		for j, body in enumerate(s):
			frame_data.append(go.Scatter3d(
				x=[body.position[0]],
				y=[body.position[1]],
				z=[body.position[2]],
				mode='markers',
				marker=dict(size=6),
				name=s[j].name
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

	return frames
