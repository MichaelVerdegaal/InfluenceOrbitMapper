import math

import arrow
import numpy as np
from PyAstronomy import pyasl

START_TIMESTAMP = '2021-04-17T14:00:00+00:00'


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


def position_at_adalia_day(rock, adalia_day):
    """
    Gets the xyz position of a rock at a set adalia day (one real day = 24 adalia days)
    :param rock: asteroid as dict
    :param adalia_day: day to check, has to be larger than 0
    :return: xyz position of asteroid
    """
    if adalia_day > 0:
        day = adalia_day % rock['orbital.T']
        orbit = setup_ellipse(rock)
        return orbit.xyzPos(day)
    else:
        return [0, 0, 0]


def position_at_adalia_day_manual(rock, adalia_day):
    """
    Direct copy of https://github.com/Influenceth/influence-utils/blob/00f6838b616d5c7113720b0f883c2a2d55a41267/index.js#L288
    Translated from JS to Python
    :param rock:
    :param adalia_day:
    :return:
    """
    a = rock['orbital.a']
    e = rock['orbital.e']
    i = rock['orbital.i']
    o = rock['orbital.o']
    w = rock['orbital.w']
    m = rock['orbital.m']

    # Calculate the longitude of perihelion
    p = w + o

    # Calculate mean motion based on assumption that mass of asteroid <<< Sun
    k = 0.01720209895  # Gaussian constant (units are days and AU)
    n = k / math.sqrt(math.pow(a, 3))  # Mean motion

    # Calcualate the mean anomoly at elapsed time
    M = m + (n * adalia_day)

    # Estimate the eccentric and true anomolies using an iterative approximation let E1let E = M let lastDiff = 1
    E1 = None
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
    orbit = setup_ellipse(rock)
    t = np.linspace(0, rock['orbital.T'], rock['orbital.T'])
    return orbit.xyzPos(t)


def get_current_adalia_day():
    """
    Get the current adalia day at current time
    :return: adalia day
    """
    start_time = arrow.get(START_TIMESTAMP)
    current_time = arrow.utcnow()
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
    start_time = arrow.get(START_TIMESTAMP)
    time = arrow.get(timestamp)
    adalia_days = (time - start_time).total_seconds() / 60 / 60
    return adalia_days
