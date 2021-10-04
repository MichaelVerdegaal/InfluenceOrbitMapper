"""Flask app creation helper."""
import os

import sass
from flask import Flask
from flask_caching import Cache
from flask_minify import minify
from viewer.config import STATIC_FOLDER

# Caching
cache = Cache(config={'CACHE_TYPE': 'simple'})
# Compile SASS to CSS
sass.compile(dirname=(os.path.join(STATIC_FOLDER, 'sass'), os.path.join(STATIC_FOLDER, 'css')),
             output_style='compressed')


def create_app():
    app = Flask(__name__, template_folder='frontend/templates/', static_folder='frontend/static/')
    minify(app=app, html=True, js=True, cssless=False)
    cache.init_app(app)
    return app
