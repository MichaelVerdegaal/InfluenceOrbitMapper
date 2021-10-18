"""Module for orbit calculations and utilities."""
import math

import numpy as np
import pendulum
import numba

START_ORBIT_TIMESTAMP = '2021-01-01T00:00:00+00:00'  # Orbit day zero
START_ARRIVAL_TIMESTAMP = '2021-04-17T14:00:00+00:00'  # Adalia day zero ("The Arrival")
# Astronomical Unit multiplier. 1 point = 1 million kilometer. Used to arrive at correct xyz pos.
AU_MULTIPLIER = 149.597871


@numba.jit(fastmath=True)
def position_at_adalia_day(a: float, e: float, i: float, o: float, w: float, m: float, aday: int):
    """
    Calculate the xyz coordinates of an asteroid at a certain adalia day.

    This function is a close to direct port from JS to Python from the influence-utils repository.
    https://github.com/Influenceth/influence-utils/blob/00f6838b616d5c7113720b0f883c2a2d55a41267/index.js#L288

    :param a: Semi-major axis
    :param e: Eccentricity
    :param i: Inclination
    :param o: Longitude of ascending node
    :param w: Argument of periapsis
    :param m: Mean anomaly at epoch
    :param aday: Adalia day to calculate position at
    :return: xyz position
    """
    # Calculate the longitude of perihelion
    p = w + o

    # Calculate mean motion based on assumption that mass of asteroid <<< Sun
    k = 0.01720209895  # Gaussian constant (units are days and AU)
    n = k / math.sqrt(math.pow(a, 3))  # Mean motion

    # Calcualate the mean anomoly at elapsed time
    M = m + (n * aday)

    # Estimate the eccentric and true anomolies using an iterative approximation
    E = M
    last_diff = 1

    while last_diff > 0.0000001:
        E1 = M + (e * math.sin(E))
        last_diff = np.abs(E1 - E)
        E = E1

    # Calculate in heliocentric polar and then convert to cartesian
    v = 2 * math.atan(math.sqrt((1 + e) / (1 - e)) * math.tan(E / 2))
    r = a * (1 - math.pow(e, 2)) / (1 + e * math.cos(v))  # Current radius in AU

    # Cartesian coordinates
    x = (r * (math.cos(o) * math.cos(v + p - o) - (math.sin(o) * math.sin(v + p - o) * math.cos(i)))) * AU_MULTIPLIER
    y = (r * (math.sin(o) * math.cos(v + p - o) + math.cos(o) * math.sin(v + p - o) * math.cos(i))) * AU_MULTIPLIER
    z = (r * math.sin(v + p - o) * math.sin(i)) * AU_MULTIPLIER
    return [x, y, z]


def get_current_position(rock):
    """
    Get the current position of an asteroid. Note that if you need to mass-calculate the current position then it's
    faster to grab the adalia day once, and use position_at_adalia_day() instead

    :param rock: asteroid as dict
    :return: xyz position as numpy array
    """
    curr_aday = get_current_adalia_day()
    orbital = rock['orbital']
    return position_at_adalia_day(orbital['a'],
                                  orbital['e'],
                                  orbital['i'],
                                  orbital['o'],
                                  orbital['w'],
                                  orbital['m'],
                                  curr_aday)


def full_position(rock):
    """
    Calculate positions vectors for the entire orbit of an asteroid.

    :param rock: asteroid as dict
    :return: position vectors as numpy array
    """
    orbital = rock['orbital']
    return [position_at_adalia_day(orbital['a'],
                                   orbital['e'],
                                   orbital['i'],
                                   orbital['o'],
                                   orbital['w'],
                                   orbital['m'],
                                   day) for day in range(rock['orbital.T'] + 1)]


def calculate_orbital_period(orbital):
    """
    Calculate orbital period of asteroid via keplers 3rd law.

    :param orbital: dict with orbital parameters
    :return: orbital period
    """
    a = orbital['a']
    third_law = 0.000007495
    return int(math.sqrt(pow(a, 3) / third_law))


def get_current_adalia_day(display_day=False):
    """
    Get the current adalia day at current time.

    :param display_day: Which timestamp to use. If true will result in the display date (such as on the website), if
    false can be used to calculate the positions in orbit
    :return: adalia day
    """
    timestamp = START_ORBIT_TIMESTAMP
    if display_day:
        timestamp = START_ARRIVAL_TIMESTAMP
    start_time = pendulum.parse(timestamp)
    current_time = pendulum.now()
    # Time diff in seconds then hours to get adalia days. 1 irl hour = 1 adalia day. Converted from seconds instead of
    # days as it's more precise.
    adalia_days = (current_time - start_time).total_seconds() / 60 / 60
    return adalia_days


def get_adalia_day_at_time(timestamp):
    """
    Get the adalia day at a specified time.

    :param timestamp: timestamp. Has to be after the START_TIMESTAMP of 2021-04-17 14:00
    :return: adalia day at date
    """
    start_time = pendulum.parse(START_ORBIT_TIMESTAMP)
    time = pendulum.parse(timestamp)
    adalia_days = (time - start_time).total_seconds() / 60 / 60
    return adalia_days


def apply_position_to_df(df):
    """Calculates xyz position for entire dataframe, requires orbital data as colum """
    curr_aday = get_current_adalia_day()
    df['pos'] = [position_at_adalia_day(x['a'],
                                        x['e'],
                                        x['i'],
                                        x['o'],
                                        x['w'],
                                        x['m'],
                                        curr_aday) for x in df['orbital']]
    return df
