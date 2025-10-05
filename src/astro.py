import numpy as np
from astroquery.jplhorizons import Horizons
from astropy.time import Time
from typing import List

from nbody import Body


def get_current_coords() -> List[Body]:
	epoch = Time.now().jd
	ret: List[Body] = []
	for name, data in solar_system_data.items():
		obj = Horizons(
			id=data['id'],
			location='@0',
			epochs=epoch
		)

		eph = obj.vectors()
		row = eph[0]

		new = Body(
			position=np.array([ # AU
				row['x'],
				row['y'],
				row['z']
			]), # * KM_TO_AU,
			velocity=np.array([ # AU/day
				row['vx'],
				row['vy'],
				row['vz']
			]), # * KM_TO_AU * SEC_TO_DAY,
			rotation=0,
			mass=data['mass_mE'],
			radius=data['radius_km'],
			name=name
		)

		print(new.position)
		ret.append(new)

	return ret

KM_TO_AU = 1 / 1.495978707e8
SEC_TO_DAY = 86400

mE_kg = 5.9724e24

solar_system_data = {
	'Sun': {
		'id': 10,
		'mass_mE': 1.9885e30 / mE_kg,
		'radius_km': 695700
	},
	'Mercury': {
		'id': 1,
		'mass_mE': 3.3011e23 / mE_kg,
		'radius_km': 2439.7
	},
	'Venus': {
		'id': 2,
		'mass_mE': 4.8675e24 / mE_kg,
		'radius_km': 6051.8
	},
	'Earth': {
		'id': 3,
		'mass_mE': 5.9724e24 / mE_kg,
		'radius_km': 6371.0
	},
	'Mars': {
		'id': 4,
		'mass_mE': 6.4171e23 / mE_kg,
		'radius_km': 3389.5
	},
	'Jupiter': {
		'id': 5,
		'mass_mE': 1.8982e27 / mE_kg,
		'radius_km': 69911
	},
	'Saturn': {
		'id': 6,
		'mass_mE': 5.6834e26 / mE_kg,
		'radius_km': 58232
	},
	'Uranus': {
		'id': 7,
		'mass_mE': 8.6810e25 / mE_kg,
		'radius_km': 25362
	},
	'Neptune': {
		'id': 8,
		'mass_mE': 1.02413e26 / mE_kg,
		'radius_km': 24622
	}
}

