"""Module for pathfinding calculations and utilities."""
from modules.asteroids import rock_name
from modules.orbits import get_current_position, AU_MULTIPLIER
from math import sqrt, pow


def calculate_routes(starting_asteroid, target_asteroids):
    """
    Calculate routes.

    :param starting_asteroid: starting asteroid
    :param target_asteroids:
    :return: dict with route information
    """
    path, time, distance = get_shortest_path(starting_asteroid, target_asteroids)
    return {'path': [a['i'] for a in path],
            'time': time,
            'distance': distance,
            'start': rock_name(path[0]),
            'target': rock_name(path[-1])
            }


def get_shortest_path(starting_asteroid, target_asteroids):
    """
    Calculate path with the shortest distance heuristic
    :param starting_asteroid: starting asteroid as dict
    :param target_asteroids: list of target asteroids as dict
    :return: path, time taken, distance
    """
    pos1 = get_current_position(starting_asteroid)

    shortest_dist = get_distance(pos1, get_current_position(target_asteroids[0]))
    closest_asteroid = target_asteroids[0]

    for asteroid in target_asteroids:
        pos2 = get_current_position(asteroid)
        dist = get_distance(pos1, pos2)
        if dist < shortest_dist:
            shortest_dist = dist
            closest_asteroid = asteroid
        print(f"Dist from {starting_asteroid['i']} to {asteroid['i']}: {dist}")
    return [starting_asteroid, closest_asteroid], '-', round(shortest_dist, 3)


def get_distance(pos1, pos2):
    """
     Calculate the distance between two 3d coordinates.

    :return: distance as float
    """
    return sqrt(pow(pos1[0] - pos2[0], 2) + pow((pos1[1] - pos2[1]), 2) + pow((pos1[2] - pos2[2]), 2))
