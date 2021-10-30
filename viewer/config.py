import os

# Project
PROJECT_FOLDER = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
APP_FOLDER = os.path.join(PROJECT_FOLDER, 'viewer')
STATIC_FOLDER = os.path.join(APP_FOLDER, 'frontend/static')
TEMPLATE_FOLDER = os.path.join(APP_FOLDER, 'frontend/templates')

