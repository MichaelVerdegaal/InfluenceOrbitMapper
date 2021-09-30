import json

from flask import render_template, abort, request
from jinja2 import TemplateNotFound

from modules.asteroids import get_roid, load_roids, radius_to_size
from modules.orbits import full_position, position_at_adalia_day, get_current_adalia_day, get_current_position
from viewer import create_app

asteroids_df = load_roids('asteroids_20210917.json')
app = create_app()  # Flask app set up like this to enable easy hosting


@app.route('/')
def home():
    try:
        return render_template("main_viewer.html")
    except TemplateNotFound:
        abort(404)


@app.route('/ajax/route', methods=['POST'])
def get_routes_calculated():
    data = request.json
    start_asteroids = data['start_asteroids']
    end_asteroids = data['target_asteroids']
    start_asteroids = [get_roid(asteroids_df, asteroid_id) for asteroid_id in start_asteroids]
    end_asteroids = [get_roid(asteroids_df, asteroid_id) for asteroid_id in end_asteroids]
    print(end_asteroids)
    response = {
        'starting_asteroids': [{'id': rock['i'],
                                'size': radius_to_size(rock['r']),
                                'name': rock['customName'] if rock['customName'] else rock['baseName'],
                                'pos': get_current_position(rock),
                                'orbit': full_position(rock)} for rock in start_asteroids],
        'target_asteroids': [{'id': rock['i'],
                              'size': radius_to_size(rock['r']),
                              'name': rock['customName'] if rock['customName'] else rock['baseName'],
                              'pos': get_current_position(rock),
                              'orbit': full_position(rock)} for rock in end_asteroids],
    }
    return json.dumps(response), 200


@app.route('/ajax/asteroid', methods=['POST'])
def get_asteroids():
    """
    AJAX endpoint to retrieve a list of asteroids
    :return: asteroids as dict, status code
    """
    data = request.json
    asteroid_id_list = data['asteroid_id_list']
    asteroids = [get_roid(asteroids_df, asteroid_id) for asteroid_id in asteroid_id_list]
    return json.dumps(asteroids), 200


@app.route('/ajax/asteroid/orbit/<int:asteroid_id>')
def get_asteroid_orbit(asteroid_id):
    """
    AJAX endpoint to retrieve an asteroid's orbit
    :param asteroid_id: asteroid id
    :return: asteroid orbit as nested list, status code
    """
    asteroid = get_roid(asteroids_df, asteroid_id)
    orbit = full_position(asteroid)
    return json.dumps(orbit), 200


@app.route('/ajax/asteroid/location/<int:asteroid_id>')
def get_asteroid_current_location(asteroid_id):
    """
    AJAX endpoint to retrieve an asteroid's current xyz location
    :param asteroid_id: asteroid id
    :return: asteroid location as list, status code
    """
    asteroid = get_roid(asteroids_df, asteroid_id)
    curr_aday = get_current_adalia_day()
    pos = position_at_adalia_day(asteroid, curr_aday)
    return json.dumps(pos), 200


@app.route('/ajax/datetime/adalia/current')
def get_adalia_day():
    """
    AJAX endpoint to retrieve the current adalia day (at time of request)
    :return: current adalia day in dict
    """
    curr_aday = get_current_adalia_day()
    return json.dumps({'day': curr_aday}), 200
