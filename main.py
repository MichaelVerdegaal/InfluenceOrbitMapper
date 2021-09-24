"""
Everything in this file is experimental for now, and will not reflect the contents of the repository when it is more
production ready.
"""
import numpy as np

from modules.asteroids import load_roids, get_roid
from modules.plotting import plot_asteroids

# Initialization
print('Booting up...')
roids = load_roids("asteroids_20210917.json")

# Get rock of choice
print("Please enter up to 10 asteroid numbers. Enter a non-number to continue")
templates = {'orbit_test': [1, 4148],  # Used to confirm correct orbit calculations via game website comparisons
             'demo': [1, 250000, 249999, 104, 235773, 13, 4148],  # Default asteroid choices
             'stress_test': np.linspace(1, 50, 50)}  # Stress test
rocks = []
while len(rocks) < 9:
    asteroid_number = input()
    if asteroid_number.isnumeric() and (0 < int(asteroid_number) <= 250000):
        rocks.append(get_roid(roids, int(asteroid_number)))
    elif asteroid_number in templates.keys():
        rocks = [get_roid(roids, i) for i in templates[asteroid_number]]
        break
    else:
        break

if not rocks:
    rocks = [get_roid(roids, i) for i in templates['demo']]
plot_asteroids(*rocks)
