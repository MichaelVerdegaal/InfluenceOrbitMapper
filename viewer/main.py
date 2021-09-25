import json

from flask import render_template, abort
from jinja2 import TemplateNotFound

from modules.asteroids import get_roid, load_roids
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
