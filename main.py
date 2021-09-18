import json
from math import sqrt, pow, degrees

import matplotlib
import matplotlib.animation as animation
import matplotlib.pylab as plt
import mpl_toolkits.mplot3d.axes3d as p3
import numpy as np
import pandas as pd
from PyAstronomy import pyasl

matplotlib.use("TkAgg")


def load_roids(json_file):
    """
    Loads asteroids from the json file
    :param json_file: json file path
    :return: dataframe
    """

    def orbital_period(a):
        """
        Calculate orbital period of asteroid via keplers 3rd law
        :param a: semi-major axis
        :return: orbital period
        """
        third_law = 0.000007495
        return int(sqrt(pow(a, 3) / third_law))

    roids = []
    with open(json_file) as f:
        for line in f:
            roids.append(json.loads(line))

    roids = pd.json_normalize(roids)  # Flatten nested JSON
    roids['orbital.T'] = roids.apply(lambda x: orbital_period(x['orbital.a']), axis=1)  # Add orbital period
    roids['orbital.i'] = roids.apply(lambda x: degrees(x['orbital.i']), axis=1)
    return roids


def get_roid(roids, id):
    """
    Get an asteroid by it's ID
    :param roids: asteroid dataframe
    :param id: id to look up
    :return: asteroid as dataframe
    """
    if 1 <= id <= 250000:
        return roids[roids['i'] == id].to_dict(orient='records')[0]


def setup_ellipse(rock):
    """
    Set up a PyAstronomy ellipse
    a: Semi-major axis
    e: Eccentricity
    i: Inclination
    o: Longitude of ascending node
    w: Argument of periapsis
    m: Mean anomoly at epoch
    T: orbital period (days)
    :param rock: asteroid as dict
    :return: KeplerEllipse object
    """
    ke = pyasl.KeplerEllipse(rock['orbital.a'],
                             rock['orbital.T'],
                             e=rock['orbital.e'],
                             Omega=rock['orbital.o'],
                             # i=rock['orbital.i'],
                             i=0.02,
                             w=rock['orbital.w'])
    return ke


# Get rock of choice
roids = load_roids("asteroids_20210811.json")
rock = get_roid(roids, 1)
print(json.dumps(rock, indent=4, sort_keys=True))

# Get rock orbit
ke = setup_ellipse(rock)
frame_count = rock['orbital.T']
t = np.linspace(0, frame_count, frame_count)
pos = ke.xyzPos(t)

# Animate orbit
fig = plt.figure()
ax = p3.Axes3D(fig)

rock_name = rock['customName'] if rock['customName'] else rock['baseName']
red_dot, = ax.plot(pos[::, 1], pos[::, 0], pos[::, 2], 'ro',
                   label=rock_name)


def animate(i, pos, red_dot):
    red_dot.set_data([pos[i][1], pos[i][0]])
    red_dot.set_3d_properties(pos[i][2])
    return red_dot,


# create animation using the animate() function
ani = animation.FuncAnimation(fig, animate, frame_count, fargs=(pos, red_dot),
                              interval=0.01, blit=False)

ax.plot([0], [0], [0], 'bo', markersize=9, label="Adalia")
ax.plot(pos[::, 1], pos[::, 0], pos[::, 2], 'k-',
        label="Satellite Trajectory")

# Hide grid and ticks
ax.grid(False)
ax.set_xticks([])
ax.set_yticks([])
ax.set_zticks([])
plt.style.use('default')
plt.legend()
plt.show()
