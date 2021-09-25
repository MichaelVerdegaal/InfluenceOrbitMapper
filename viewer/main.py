from flask import render_template, abort
from jinja2 import TemplateNotFound

from viewer import create_app

app = create_app()  # Flask app set up like this to enable easy hosting


@app.route('/')
def home():
    try:
        return render_template("main_viewer.html")
    except TemplateNotFound:
        abort(404)
