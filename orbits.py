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
    # Time diff in seconds then hours to get adalia days. 1 irl hour = 1 adalia day. Converted from seconds
    # as it's more precise.
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
