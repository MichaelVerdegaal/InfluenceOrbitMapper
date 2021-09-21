"""
Everything in this file is experimental for now, and will not reflect the contents of the repository when it is more
production ready.
"""

import matplotlib

from asteroids import load_roids, get_roid
from orbits import reverse_search_starting_orbit_day
from plotting import plot_asteroid_paths

# Initialization
print('Booting up...')
matplotlib.use("TkAgg")  # Use the Tkinter backend to display animations
roids = load_roids("asteroids_20210917.json")

# Get rock of choice
rock_1 = get_roid(roids, 1)
rock_2 = get_roid(roids, 249999)

# print('Plotting rocks')
# plot_asteroid_paths(rock_1, rock_2)

# Attempt at reverse engineering coord matching
reverse_search_starting_orbit_day(rock_1)
reverse_search_starting_orbit_day(rock_2)
