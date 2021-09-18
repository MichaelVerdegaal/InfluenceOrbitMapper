import json
from math import sqrt, pow

import matplotlib.pylab as plt
import numpy as np
import pandas as pd
from PyAstronomy import pyasl


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
        return sqrt(pow(a, 3) / third_law)

    roids = []
    with open(json_file) as f:
        for line in f:
            roids.append(json.loads(line))

    roids = pd.json_normalize(roids)  # Flatten nested JSON
    roids['orbital.T'] = roids.apply(lambda x: orbital_period(x['orbital.a']), axis=1)  # Add orbital period
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
                             i=rock['orbital.i'],
                             w=rock['orbital.w'])
    return ke


roids = load_roids("asteroids_20210811.json")
rock = get_roid(roids, 1)

ke = setup_ellipse(rock)
t = np.linspace(0, 4, 200)
pos = ke.xyzPos(t)

plt.plot(0, 0, 'bo', markersize=9, label="Sun")
plt.plot(pos[::, 1], pos[::, 0], 'k-', label="Satellite Trajectory")
plt.plot(pos[0, 1], pos[0, 0], 'r*', label="Periapsis")
plt.legend(loc="upper right")
plt.title('Orbital Simulation')
plt.show()
