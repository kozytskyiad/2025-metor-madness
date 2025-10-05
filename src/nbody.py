import numpy as np
from numpy.typing import NDArray
from scipy.spatial import distance
from dataclasses import dataclass
from typing import List, Tuple, Optional


@dataclass
class Simulation:
	G: float = 6.67430e-11
	dt: float = 0.01

@dataclass
class Body:
	position: NDArray[np.float64]
	velocity: NDArray[np.float64]
	rotation: float
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
			rotation=body.rotation,
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

def _line_sphere_roots(
	ray_origin: NDArray[np.float64],
	ray_direction: NDArray[np.float64],
	sphere_center: NDArray[np.float64],
	sphere_radius: float
) -> Optional[Tuple[float, float]]:
	oc = ray_origin - sphere_center
	a = np.dot(ray_direction, ray_direction)
	b = 2 * np.dot(oc, ray_direction)
	c = np.dot(oc, oc) - sphere_radius**2

	discr = b*b - 4*a*c
	if discr == 0:
		t = -b / (2*a)
		return (t,t)
	elif discr > 0:
		sqrt_discr = np.sqrt(discr)
		t1 = (-b - sqrt_discr) / (2*a)
		t2 = (-b + sqrt_discr) / (2*a)
		return (min(t1, t2), max(t1, t2))

	return None

def point_sphere_collision(
	point_body: Tuple[Body, Body],
	sphere_body: Tuple[Body, Body],
	params: Simulation
) -> Optional[Tuple[float, NDArray[np.float64]]]:
	pbtm1, pbt = point_body
	sbtm1, sbt = point_body

	if sbtm1.radius <= 0:
		raise ValueError('Sphere must have a positive radius')
	if pbtm1.name == sbtm1.name:
		raise ValueError('Cannot check collision of a body with itself')

	point_seg_start, point_seg_end = pbtm1.position, pbt.position
	sphere_seg_start, sphere_seg_end = sbtm1.position, sbt.position

	rel_origin = point_seg_start - sphere_seg_start
	rel_displacement = (point_seg_end - point_seg_start) \
	                   - (sphere_seg_end - sphere_seg_start)

	t_roots = _line_sphere_roots(
		ray_origin,
		ray_direction,
		np.array([0,0,0], dtype=np.float64),
		sbtm1.radius
	)

	if t_roots is None: return None

	t1, t2 = t_roots

	valid_t_frac = []
	if -epsilon <= t1 <= (1 + epsilon):
		valid_t_frac.append(t1)
	if -epsilon <= t2 <= (1 + epsilon):
		valid_t_frac.append(t2)

	if not valid_t_frac: return None

	dist_tm1 = distance.euclidean(point_seg_start, sphere_seg_start)
	init_inside = dist_tm1 <= (sbtm1.radius + params.dt)

	collision_t_frac = None
	if init_inside:
		pos_valid_t = [t for t in valid_v_frac if t >= -params.dt]
		if pos_valid_t:
			collision_t_frac = min(pos_valid_t)
	else:
		pos_valid_t = [t for t in valid_t_frac if t >= -params.dt]
		if pos_valid_t:
			collision_t_frac = min(pos_valid_t)

	if collision_t_frac is not None:
		glob_coll_point = point_seg_start \
			+ collision_t_frac * (point_seg_end - point_seg_start)
		return collision_t_frac, glob_coll_point

	return None

