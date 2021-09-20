import json
from math import sqrt, pow, degrees

import pandas as pd


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
    # roids['orbital.i'] = roids.apply(lambda x: degrees(x['orbital.i']), axis=1)  # Convert inclination radian to degrees
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
    else:
        raise SyntaxWarning("Improper asteroid ID")
