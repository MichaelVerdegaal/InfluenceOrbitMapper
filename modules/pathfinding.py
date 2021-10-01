from modules.asteroids import rock_name

def time_flying():
    """
    Dummy function to calculate time spent flying
    :return: time as float
    """
    return 5


def get_distance():
    """
    Dummy function to calculate the distance between two coordinates
    :return: distance as float
    """
    return 1000


def calculate_routes(starting_asteroid, target_asteroids):
    """
    Dummy function to calculate routes
    :param starting_asteroid: starting asteroid
    :param target_asteroids:
    :return: dict with route information
    """
    return {'path': [starting_asteroid['i'], 50, target_asteroids[0]['i']],
            'time': '2 hours, 4 minutes',
            'distance': 100,
            'start': rock_name(starting_asteroid),
            'target': rock_name(target_asteroids[0])
            }
