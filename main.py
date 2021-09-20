"""
Everything in this file is experimental for now, and will not reflect the contents of the repository when it is more
production ready.
"""

import matplotlib

from asteroids import load_roids, get_roid
from orbits import position_at_adalia_day_manual

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
def reverse_search_original_T(rock):
    x, y, z = rock['p.x'], rock['p.y'], rock['p.z']
    T = rock['orbital.T']

    print(f"\n\nExpected XYZ coords of {rock['baseName']}: [{rock['p.x']}, {rock['p.y']}, "
          f"{rock['p.z']}] with orbital period {T}\n")

    listy = []
    for day in range(T):
        pos = position_at_adalia_day_manual(rock, day)
        x1_round, x2_round = round(pos[0], 2), round(x, 2)
        x_match = x1_round == x2_round
        y1_round, y2_round = round(pos[1], 2), round(y, 2)
        y_match = y1_round == y2_round
        z1_round, z2_round = round(pos[2], 2), round(z, 2)
        z_match = z1_round == z2_round
        if x_match and y_match and z_match:
            listy.append({'T': day, 'p': pos})

    print(f"{len(listy)} coord match!")
    for i in listy:
        print(i)


reverse_search_original_T(rock_1)
reverse_search_original_T(rock_2)
