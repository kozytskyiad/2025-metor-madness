import numpy as np
from numpy.typing import NDArray
from dataclasses import dataclass
from typing import List, Tuple

@dataclass
class Simulation:
	G: float = 6.67430e-11
	dt: float = 0.01

@dataclass
class Body:
	position: NDArray[np.float64]
	velocity: NDArray[np.float64]
	mass: float
	radius: float
	name: str

	def __eq__(self, other):
		if isinstance(other, Body): return self.name == other.name
		return NotImplemented

	def __ne__(self, other):
		return not self.__eq__(other)

def nbody_step(
	bodies: List[Body],
	param: Simulation
) -> List[Body]:
	ret: List[Body] = []
	for body in bodies:
		body: Body
		force = np.zeros(3, dtype=np.float64)
		for other in bodies:
			other: Body
			if body == other: continue
			r_vec = body.position - other.position
			r_mag = np.linalg.norm(r_vec)**2
			if r_mag > 1e-10:
				force -= param.G * body.mass * other.mass * r_vec / r_mag
		acc = force / body.mass

		new_vel = body.velocity + acc * param.dt
		new_pos = body.position + new_vel * param.dt

		ret.append(Body(
			position=new_pos,
			velocity=new_vel,
			mass=body.mass,
			radius=body.radius,
			name=body.name
		))

	return ret

def nbody_sim(
	bodies: List[Body],
	steps: int,
	param: Simulation
) -> List[List[Body]]:
	ret: List[List[Body]] = []
	cur: List[Body] = bodies.copy()
	for i in range(steps):
		cur = nbody_step(cur, param)
		ret.append(cur)

	return ret
