import math

import numpy as np
import pendulum

START_ORBIT_TIMESTAMP = '2021-01-01T00:00:00+00:00'  # Orbit day zero
START_ARRIVAL_TIMESTAMP = '2021-04-17T14:00:00+00:00'  # Adalia day zero ("The Arrival")


def position_at_adalia_day(rock, adalia_day):
    """
    Calculates the xyz coordinates of an asteroid at a certain adalia day. Direct copy of
    https://github.com/Influenceth/influence-utils/blob/00f6838b616d5c7113720b0f883c2a2d55a41267/index.js#L288
    Translated from JS to Python.
    :param rock: asteroid as dict
    :param adalia_day: adalia day to calculate from
    :return: xyz position as numpy array
    """
    a = rock['orbital.a']
    e = rock['orbital.e']
    i = rock['orbital.i']
    o = rock['orbital.o']
    w = rock['orbital.w']
    m = rock['orbital.m']
    adalia_day = adalia_day % rock['orbital.T']

    # Calculate the longitude of perihelion
    p = w + o

    # Calculate mean motion based on assumption that mass of asteroid <<< Sun
    k = 0.01720209895  # Gaussian constant (units are days and AU)
    n = k / math.sqrt(math.pow(a, 3))  # Mean motion

    # Calcualate the mean anomoly at elapsed time
    M = m + (n * adalia_day)

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
    x = r * (math.cos(o) * math.cos(v + p - o) - (math.sin(o) * math.sin(v + p - o) * math.cos(i)))
    y = r * (math.sin(o) * math.cos(v + p - o) + math.cos(o) * math.sin(v + p - o) * math.cos(i))
    z = r * math.sin(v + p - o) * math.sin(i)
    return np.array([x, y, z])


def full_position(rock):
    """
    Calculate positions vectors for the entire orbit of an asteroid
    :param rock: asteroid as dict
    :return: position vectors as numpy array
    """
    return np.array([position_at_adalia_day(rock, day) for day in range(rock['orbital.T'] + 1)])


def calculate_orbital_period(a):
    """
    Calculate orbital period of asteroid via keplers 3rd law
    :param a: semi-major axis
    :return: orbital period
    """
    third_law = 0.000007495
    return int(math.sqrt(pow(a, 3) / third_law))


def get_current_adalia_day(display_day=False):
    """
    Get the current adalia day at current time
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
    Get the  adalia day at a specified time
    :param timestamp: timestamp. Has to be after the START_TIMESTAMP of 2021-04-17 14:00
    :return: adalia day at date
    """
    start_time = pendulum.parse(START_ORBIT_TIMESTAMP)
    time = pendulum.parse(timestamp)
    adalia_days = (time - start_time).total_seconds() / 60 / 60
    return adalia_days
