"""Flask launcher file with endpoints."""
import ujson
from flask import render_template, abort, request
from jinja2 import TemplateNotFound

from modules.asteroids import get_roid, load_roids, radius_to_size, rock_name
from modules.orbits import full_position, get_current_position
from viewer import create_app

asteroids_df = load_roids('asteroids_20210917.json')
app = create_app()  # Flask app set up like this to enable easy hosting

from modules.pathfinding import calculate_routes  # Is below asteroids_df to prevent circular import


@app.route('/')
def home():
    """
    Render home page.

    :return: html page
    """
    try:
        return render_template("main_viewer.html")
    except TemplateNotFound:
        abort(404)


@app.route('/ajax/route', methods=['POST'])
def get_routes_calculated():
    """
    AJAX endpoint to calculate routes between start and target asteroids.

    :return: calculated routes and asteroid information as dict, status code
    """

    def pack_path_dict(asteroid_list):
        """Packs the asteroids into a list of dicts, including the position and path"""
        return [{**rock,
                 'size': radius_to_size(rock['r']),
                 'name': rock_name(rock),
                 'pos': get_current_position(rock),
                 'orbit': full_position(rock)} for rock in asteroid_list]

    data = request.json
    start_asteroids = data['start_asteroids']
    target_asteroids = data['target_asteroids']
    heuristic = data['heuristic']

    start_asteroids = [get_roid(asteroids_df, asteroid_id) for asteroid_id in start_asteroids]
    target_asteroids = [get_roid(asteroids_df, asteroid_id) for asteroid_id in target_asteroids]

    route = calculate_routes(start_asteroids[0], target_asteroids, heuristic)
    travel_asteroids = [get_roid(asteroids_df, asteroid_id) for asteroid_id in route['path']]

    response = {
        'starting_asteroids': pack_path_dict(start_asteroids),
        'target_asteroids': pack_path_dict(target_asteroids),
        'travel_asteroids': pack_path_dict(travel_asteroids),
        'route': route
    }
    return ujson.dumps(response), 200
