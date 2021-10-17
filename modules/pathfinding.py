"""Module for pathfinding calculations and utilities."""

import math

from scipy.spatial.distance import cdist

from modules.astar import find_path
from modules.asteroids import rock_name
from viewer.main import asteroids_df


def sphere_neighbours(df, current_asteroid, radius=100):
    """
    Gets the neighbours of the current asteroid in a spherical radius

    :param df: Dataframe view. Has to contain [i, orbital.T, pos]
    :param current_asteroid: asteroid to select neighbours from
    :param radius: in which radius (euclidian) to consider the rocks as neighbours
    :return: list of dicts of neighbouring asteroids
    """
    # Init
    index_exclusion = df.index.isin([current_asteroid['i']])
    df = df[~index_exclusion]

    # Filters out asteroids that are already way out of range
    current_orbital_period = current_asteroid['orbital.T']
    orbital_range = 1000
    filtered_df = df.loc[df['orbital.T'].between(current_orbital_period - orbital_range,
                                                 current_orbital_period + orbital_range)]

    # Get xyz coords for filtered asteroids
    cur_pos = current_asteroid['pos']
    pos_list = filtered_df['pos'].to_list()

    # Calculate rocks within spherical range
    dist = cdist(pos_list, [cur_pos], metric='euclidean')
    mask = dist <= radius
    neighbours_df = filtered_df.loc[mask]
    return neighbours_df.to_dict('records')


def calculate_routes(starting_asteroid, target_asteroids, heuristic):
    """
    Calculate routes.

    :param starting_asteroid: starting asteroid
    :param target_asteroids: target asteroids
    :param heuristic: cost function of choice
    :return: dict with route information
    """
    df = asteroids_df[['i', 'orbital.T', 'pos']]
    path = find_path(starting_asteroid,
                     target_asteroids[0],
                     neighbors_fnct=lambda a: sphere_neighbours(df, a),
                     heuristic_cost_estimate_fnct=asteroid_distance,
                     distance_between_fnct=asteroid_distance,
                     is_goal_reached_fnct=lambda a, b: a['i'] == b['i'])

    print(f"Path = {' --> '.join([str(r['i']) for r in path])}")
    return {'path': [r['i'] for r in path],
            'time': 'time',
            'distance': 100,
            'start': rock_name(starting_asteroid),
            'target': rock_name(target_asteroids[0])
            }


def asteroid_distance(a1, a2):
    """
    Helper function used in astar to get the distance of asteroids

    :param a1: asteroid dict
    :param a2: asteroid dict
    :return: distance as float
    """
    pos1 = a1['pos']
    pos2 = a2['pos']
    return euclidian(pos1, pos2)


def euclidian(pos1, pos2):
    """
    Calculate the euclidian distance between two cartesian coordinates.

    @param pos1: list of xyz coordinates
    @param pos2: list of xyz coordinates
    :return: distance as float
    """
    return math.sqrt(sum((e1 - e2) ** 2 for e1, e2 in zip(pos1, pos2)))
