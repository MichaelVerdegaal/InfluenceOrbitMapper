"""Module for asteroid utilities."""
import json

import pandas as pd

from modules.orbits import calculate_orbital_period

SIZES = ['SMALL', 'MEDIUM', 'LARGE', 'HUGE']


def load_roids(json_file):
    """
    Load asteroids from the source file.

    :param json_file: json file path
    :return: dataframe
    """
    roids = []
    with open(json_file) as f:
        for line in f:
            unpacked_line = json.loads(line)
            roids.append({'i': unpacked_line['i'],
                          'r': unpacked_line['r'],
                          'baseName': unpacked_line['baseName'],
                          'spectralType': unpacked_line['spectralType'],
                          'orbital': unpacked_line['orbital'],
                          'customName': unpacked_line.get('customName', '')})

    roids = pd.json_normalize(roids)  # Flatten nested JSON
    roids['orbital.T'] = roids.apply(lambda x: calculate_orbital_period(x['orbital.a']), axis=1)  # Orbital period
    return roids


def get_roid(roids, rock_id):
    """
    Get an asteroid by its ID.

    :param roids: asteroid dataframe
    :param rock_id: id to look up
    :return: asteroid as dataframe
    """
    if 1 <= rock_id <= 250000:
        return roids[roids['i'] == rock_id].to_dict(orient='records')[0]
    else:
        raise SyntaxWarning("Improper asteroid ID")


def radius_to_size(radius):
    """
    Convert asteroid radius to size category.

    :param radius: radius
    :return: category as string
    """
    if radius <= 5000:
        return SIZES[0]
    elif radius <= 20000:
        return SIZES[1]
    elif radius <= 50000:
        return SIZES[2]
    else:
        return SIZES[3]


def rock_name(asteroid):
    """
    Return the proper display name for an asteroid name, with the custom one taking priority.

    :param asteroid: asteroid as dict
    :return: name as string
    """
    return asteroid['customName'] if asteroid['customName'] else asteroid['baseName']
