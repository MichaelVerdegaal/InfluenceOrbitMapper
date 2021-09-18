import json

import matplotlib
import numpy as np

from asteroids import load_roids, get_roid
from orbits import setup_ellipse, animate_single_orbit

matplotlib.use("TkAgg")  # Use the Tkinter backend to display animations

# Get rock of choice
roids = load_roids("asteroids_20210917.json")
rock = get_roid(roids, 1)

# Get rock orbit
ke = setup_ellipse(rock)
frame_count = rock['orbital.T']
t = np.linspace(0, frame_count, frame_count)
pos = ke.xyzPos(t)

# Animate orbit
animate_single_orbit(rock, pos, frame_count)
