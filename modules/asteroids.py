"""Module for asteroid utilities."""
import pandas as pd
import ujson

from modules.orbits import calculate_orbital_period, apply_position_to_df

SIZES = ['SMALL', 'MEDIUM', 'LARGE', 'HUGE']


def load_asteroids(json_file: str):
    """
    Load asteroids from the source file.

    :param json_file: json file name (path)
    :return: dataframe
    """
    json_asteroids = []
    with open(json_file) as f:
        for line in f:
            unpacked_line = ujson.loads(line)
            json_asteroids.append({'i': unpacked_line['i'],
                                   'r': unpacked_line['r'],
                                   'baseName': unpacked_line['baseName'],
                                   'orbital': unpacked_line['orbital'],
                                   'customName': unpacked_line.get('customName', '')})

    asteroids_df = pd.DataFrame(json_asteroids)  # Flatten nested JSON
    asteroids_df['orbital.T'] = [calculate_orbital_period(x) for x in asteroids_df['orbital']]  # Orbital period
    asteroids_df.set_index('i', inplace=True, drop=False)  # Set asteroid ID as index

    asteroids_df = asteroids_df.astype({'i': 'int32',
                                        'r': 'int32',
                                        'orbital.T': 'int16'})  # Reduce int limit to save memory
    asteroids_df = apply_position_to_df(asteroids_df)
    return asteroids_df


def get_asteroid(df: pd.DataFrame, asteroid_id: int):
    """
    Get an asteroid by its ID.

    :param df: asteroid dataframe
    :param asteroid_id: id to look up
    :return: asteroid as dict
    """
    if 1 <= asteroid_id <= 250000:
        return df.loc[asteroid_id].to_dict()
    else:
        raise SyntaxWarning("Improper asteroid ID")


def radius_to_size(radius: int):
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


def asteroid_name(asteroid: dict):
    """
    Return the proper display name for an asteroid name, with the custom one taking priority.

    :param asteroid: asteroid of choice
    :return: name as string
    """
    return asteroid['customName'] if asteroid['customName'] else asteroid['baseName']


asteroids_df = load_asteroids('asteroids_20210917.json')
