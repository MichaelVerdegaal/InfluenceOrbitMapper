import matplotlib

from asteroids import load_roids, get_roid
from plotting import plot_asteroid_paths

# Initialization
print('Booting up...')
matplotlib.use("TkAgg")  # Use the Tkinter backend to display animations
roids = load_roids("asteroids_20210917.json")

# Get rock of choice
adalia_prime = get_roid(roids, 1)
saturnus = get_roid(roids, 249999)

# print('Plotting rocks')
plot_asteroid_paths(saturnus, adalia_prime)