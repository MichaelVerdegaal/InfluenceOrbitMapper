"""
Everything in this file is experimental for now, and will not reflect the contents of the repository when it is more
production ready.
"""

from asteroids import load_roids, get_roid
from plotting import plot_asteroids

# Initialization
print('Booting up...')
roids = load_roids("asteroids_20210917.json")

# Get rock of choice
rock_1 = get_roid(roids, 1)  # Adalia prime
rock_2 = get_roid(roids, 250000)  # Very far away
rock_3 = get_roid(roids, 235773)  # Extremely high inclination/eccentricity
rock_4 = get_roid(roids, 13)
rock_5 = get_roid(roids, 87)

plot_asteroids(rock_1, rock_2, rock_3, rock_4, rock_5)



