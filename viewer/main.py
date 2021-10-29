"""Flask launcher file with endpoints."""
import ujson
from jinja2 import TemplateNotFound
from quart import render_template, abort, request

from modules.asteroids import get_roid, asteroids_df, radius_to_size, rock_name
from modules.orbits import full_position, get_current_position
from viewer import create_app

app = create_app()  # We set up the app as a variable as this allows more convenience for running the server

from modules.pathfinding import calculate_routes  # Is below asteroids_df to prevent circular import


@app.route('/')
async def home():
    """
    Render home page.

    :return: html page
    """
    try:
        return await render_template("main_viewer.html")
    except TemplateNotFound:
        abort(404)


@app.route('/ajax/route', methods=['POST'])
async def get_routes_calculated():
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

    data = await request.json
    start_asteroid_ids = data['start_asteroids']
    target_asteroids_ids = data['target_asteroids']
    heuristic = data['heuristic']

    start_asteroids = [get_roid(asteroids_df, asteroid_id) for asteroid_id in start_asteroid_ids]
    target_asteroids = [get_roid(asteroids_df, asteroid_id) for asteroid_id in target_asteroids_ids]

    route = calculate_routes(start_asteroids[0], target_asteroids, heuristic)
    travel_list = [i for i in route['path'] if i not in (start_asteroid_ids + target_asteroids_ids)]
    travel_asteroids = [get_roid(asteroids_df, asteroid_id) for asteroid_id in travel_list]

    response = {
        'starting_asteroids': pack_path_dict(start_asteroids),
        'target_asteroids': pack_path_dict(target_asteroids),
        'travel_asteroids': pack_path_dict(travel_asteroids),
        'route': route
    }
    return ujson.dumps(response), 200
