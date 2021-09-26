import json

from flask import render_template, abort
from jinja2 import TemplateNotFound

from modules.asteroids import get_roid, load_roids
from modules.orbits import full_position, position_at_adalia_day, get_current_adalia_day
from viewer import create_app

asteroids = load_roids('asteroids_20210917.json')
app = create_app()  # Flask app set up like this to enable easy hosting


@app.route('/')
def home():
    try:
        return render_template("main_viewer.html")
    except TemplateNotFound:
        abort(404)


@app.route('/ajax/asteroid/<int:asteroid_id>')
def get_asteroid(asteroid_id):
    """
    AJAX endpoint to retrieve an asteroid
    :param asteroid_id: asteroid id
    :return: asteroid as dict, status code
    """
    asteroid = get_roid(asteroids, asteroid_id)
    return json.dumps(asteroid), 200


@app.route('/ajax/asteroid/orbit/<int:asteroid_id>')
def get_asteroid_orbit(asteroid_id):
    """
    AJAX endpoint to retrieve an asteroid's orbit
    :param asteroid_id: asteroid id
    :return: asteroid orbit as nested list, status code
    """
    asteroid = get_roid(asteroids, asteroid_id)
    orbit = full_position(asteroid)
    orbit = [list(pos) for pos in orbit]
    return json.dumps(orbit), 200


@app.route('/ajax/asteroid/location/<int:asteroid_id>')
def get_asteroid_current_location(asteroid_id):
    """
    AJAX endpoint to retrieve an asteroid's current xyz location
    :param asteroid_id: asteroid id
    :return: asteroid location as list, status code
    """
    asteroid = get_roid(asteroids, asteroid_id)
    curr_aday = get_current_adalia_day()
    pos = position_at_adalia_day(asteroid, curr_aday)
    return json.dumps(list(pos)), 200


@app.route('/ajax/datetime/adalia/current')
def get_adalia_day():
    """
    AJAX endpoint to retrieve the current adalia day (at time of request)
    :return: current adalia day in dict
    """
    curr_aday = get_current_adalia_day()
    return json.dumps({'day': curr_aday}), 200

