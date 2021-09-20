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
rock_2 = get_roid(roids, 249999)

# print('Plotting rocks')
# plot_asteroid_paths(rock_1, rock_2)

x, y, z = rock_1['p.x'], rock_1['p.y'], rock_1['p.z']
T = rock_1['orbital.T']
print(f"Expected XYZ coords of {rock_1['customName']}:[{rock_1['p.x']}, {rock_1['p.y']}, {rock_1['p.z']}] "
      f"with orbital period {T}\n")

# Attempt at reverse engineering the orbit calculation
listy = []
for day in range(T * 24):
    pos = position_at_adalia_day_manual(rock_1, day)
    x1_round, x2_round = round(pos[0], 2), round(x, 2)
    x_match = x1_round == x2_round
    y1_round, y2_round = round(pos[1], 2), round(y, 2)
    y_match = y1_round == y2_round
    z1_round, z2_round = round(pos[2], 2), round(z, 2)
    z_match = z1_round == z2_round
    if x_match and y_match and z_match:
        listy.append({'T': day, 'p': pos, 'true': [x, y, z]})

for i in listy:
    print(i)
print(len(listy))
