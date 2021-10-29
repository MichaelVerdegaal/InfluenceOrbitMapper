"""Flask app creation helper."""
import os

import sass
from quart import Quart
# from flask_caching import Cache
# from flask_minify import minify
from viewer.config import STATIC_FOLDER

# Caching
# TODO: Handle these middleware
# cache = Cache(config={'CACHE_TYPE': 'simple'})
# Compile SASS to CSS
sass.compile(dirname=(os.path.join(STATIC_FOLDER, 'sass'), os.path.join(STATIC_FOLDER, 'css')),
             output_style='compressed')


def create_app():
    app = Quart(__name__, template_folder='frontend/templates/', static_folder='frontend/static/')
    # TODO: Handle these middleware
    # minify(app=app, html=True, js=True, cssless=False)
    # cache.init_app(app)
    return app
