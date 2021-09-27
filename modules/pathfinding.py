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
    :return:
    """
    route_list = []
    for target in target_asteroids:
        route = {'path': [1, 2],
                 'distance': get_distance(),
                 'time': time_flying()}
        route_list.append(route)
    return route_list
