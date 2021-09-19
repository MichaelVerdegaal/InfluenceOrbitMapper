import matplotlib
import numpy as np

from asteroids import load_roids, get_roid
from orbits import *

matplotlib.use("TkAgg")  # Use the Tkinter backend to display animations

# Get rock of choice
roids = load_roids("asteroids_20210917.json")
rock = get_roid(roids, 1)

# print(position_at_adalia_day(rock, 3705.87))
print(get_current_adalia_day())