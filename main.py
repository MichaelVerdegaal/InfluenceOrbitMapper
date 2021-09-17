import json
from math import sqrt, pow
import pandas as pd

"""
a: Semi-major axis
e: Eccentricity
i: Inclination
o: Longitude of ascending node
w: Argument of periapsis
m: Mean anomoly at epoch
T: orbital period (days)
"""


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
        return roids[roids['i'] == id]


roids = load_roids("asteroids_20210811.json")
A = get_roid(roids, 1)
print(5)
