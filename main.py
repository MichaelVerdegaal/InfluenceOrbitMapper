"""
Everything in this file is experimental for now, and will not reflect the contents of the repository when it is more
production ready.
"""

from modules.asteroids import load_roids, get_roid
from modules.plotting import plot_asteroids

# Initialization
print('Booting up...')
roids = load_roids("asteroids_20210917.json")

# Get rock of choice
rocks = [
    get_roid(roids, 1),  # Adalia prime
    get_roid(roids, 250000),  # Very far away
    get_roid(roids, 235773),  # Extremely high inclination/eccentricity
    get_roid(roids, 104),
    get_roid(roids, 249999)
]


plot_asteroids(*rocks)
