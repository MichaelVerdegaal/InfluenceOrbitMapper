"""Flask app creation helper."""
import quart.flask_patch  # Must be top level to patch Flask extensiosn
import os

import sass
from flask_caching import Cache
from quart import Quart

from viewer.config import STATIC_FOLDER, TEMPLATE_FOLDER


# Caching
cache = Cache(config={'CACHE_TYPE': 'simple'})
# Compile SASS to CSS
sass.compile(dirname=(os.path.join(STATIC_FOLDER, 'sass'), os.path.join(STATIC_FOLDER, 'css')),
             output_style='compressed')


def create_app():
    app = Quart(__name__, template_folder=TEMPLATE_FOLDER, static_folder=STATIC_FOLDER)
    cache.init_app(app)
    return app
