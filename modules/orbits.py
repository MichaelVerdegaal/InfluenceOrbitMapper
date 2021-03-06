"""Module for orbit calculations and utilities."""

import numpy as np
import pandas as pd
import pendulum
import numba as nb
from math import sqrt, pow, cos, sin, tan, atan

START_ORBIT_TIMESTAMP = '2021-01-01T00:00:00+00:00'  # Orbit day zero
START_ARRIVAL_TIMESTAMP = '2021-04-17T14:00:00+00:00'  # Adalia day zero ("The Arrival")
# Inflation multiplier, used to increase the size of a position for better visual clarity. Number is based of AU
INFLATE_MULTIPLIER = 149.597871


@nb.jit(nopython=True, fastmath=True)
def position_at_adalia_day(a: float, e: float, i: float, o: float, w: float, m: float, aday: int, inflate: bool = True):
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
    :param inflate: inflate pos for visual purposes
    :return: xyz position
    """
    # Calculate the longitude of perihelion
    p = w + o

    # Calculate mean motion based on assumption that mass of asteroid <<< Sun
    k = 0.01720209895  # Gaussian constant (units are days and AU)
    n = k / sqrt(pow(a, 3))  # Mean motion

    # Calcualate the mean anomoly at elapsed time
    M = m + (n * aday)

    # Estimate the eccentric and true anomolies using an iterative approximation
    E = M
    last_diff = 1

    while last_diff > 0.0000001:
        E1 = M + (e * sin(E))
        last_diff = np.abs(E1 - E)
        E = E1

    # Calculate in heliocentric polar and then convert to cartesian
    v = 2 * atan(sqrt((1 + e) / (1 - e)) * tan(E / 2))
    r = a * (1 - pow(e, 2)) / (1 + e * cos(v))  # Current radius in AU

    # Cartesian coordinates
    x = (r * (cos(o) * cos(v + p - o) - (sin(o) * sin(v + p - o) * cos(i))))
    y = (r * (sin(o) * cos(v + p - o) + cos(o) * sin(v + p - o) * cos(i)))
    z = (r * sin(v + p - o) * sin(i))
    return [x * INFLATE_MULTIPLIER, y * INFLATE_MULTIPLIER, z * INFLATE_MULTIPLIER] if inflate else [x, y, z]


def get_current_position(asteroid: dict):
    """
    Get the current position of an asteroid. Note that if you need to mass-calculate the current position then it's
    faster to grab the adalia day once, and use position_at_adalia_day() instead

    :param asteroid: asteroid of selection
    :return: xyz position as list
    """
    curr_aday = get_current_adalia_day()
    orbital = asteroid['orbital']
    return position_at_adalia_day(orbital['a'],
                                  orbital['e'],
                                  orbital['i'],
                                  orbital['o'],
                                  orbital['w'],
                                  orbital['m'],
                                  curr_aday)


def full_position(asteroid: dict):
    """
    Calculate position vectors for the entire orbit of an asteroid.

    :param asteroid: asteroid of choice
    :return: position vectors as numpy array
    """
    orbital = asteroid['orbital']
    return [position_at_adalia_day(orbital['a'],
                                   orbital['e'],
                                   orbital['i'],
                                   orbital['o'],
                                   orbital['w'],
                                   orbital['m'],
                                   day) for day in range(asteroid['orbital.T'] + 1)]


@nb.njit(fastmath=True)
def calculate_orbital_period(a: float):
    """
    Calculate orbital period of asteroid via keplers 3rd law.

    :param a: semi-major axis
    :return: orbital period
    """
    third_law = 0.000007495
    return int(sqrt(pow(a, 3) / third_law))


def get_current_adalia_day(display_day: bool = False):
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


def get_adalia_day_at_time(timestamp: str):
    """
    Get the adalia day at a specified time.

    :param timestamp: timestamp. Has to be after the START_TIMESTAMP of 2021-04-17 14:00
    :return: adalia day at date
    """
    start_time = pendulum.parse(START_ORBIT_TIMESTAMP)
    time = pendulum.parse(timestamp)
    adalia_days = (time - start_time).total_seconds() / 60 / 60
    return adalia_days


def apply_position_to_df(df: pd.DataFrame):
    """
    Calculates xyz position for entire dataframe, requires orbital data as column

    :param df: dataframe to apply column to
    :return: dataframe
    """
    curr_aday = get_current_adalia_day()
    df['pos'] = [position_at_adalia_day(x['a'],
                                        x['e'],
                                        x['i'],
                                        x['o'],
                                        x['w'],
                                        x['m'],
                                        curr_aday) for x in df['orbital']]
    return df
