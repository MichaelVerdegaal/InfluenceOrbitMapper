import matplotlib

from asteroids import load_roids, get_roid
from plotting import plot_asteroid_paths
from orbits import position_at_adalia_day, position_at_adalia_day_manual

# Initialization
print('Booting up...')
matplotlib.use("TkAgg")  # Use the Tkinter backend to display animations
roids = load_roids("asteroids_20210917.json")

# Get rock of choice
rock_1 = get_roid(roids, 1)

# print('Plotting rocks')
# plot_asteroid_paths(saturnus, adalia_prime)

x, y, z = rock_1['p.x'], rock_1['p.y'], rock_1['p.z']
T = rock_1['orbital.T']
print(f"Expected XYZ coords of {rock_1['customName']}:[{rock_1['p.x']}, {rock_1['p.y']}, {rock_1['p.z']}] "
      f"with orbital period {T}\n")

# Attempt at reverse engineering the orbit calculation
listy = []
for day in range(T * 24):
    pos = position_at_adalia_day_manual(rock_1, day)
    x1_round, x2_round = round(pos[0], 3), round(x, 3)
    x_delta = x1_round == x2_round
    if x_delta:
        listy.append({'T': day, 'p': pos, 'true': [x, y, z]})

for i in listy:
    print(i)
print(len(listy))
