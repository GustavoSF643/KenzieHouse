from flask import Flask, Blueprint
from . import users_routes

bp_api = Blueprint('api_bp', __name__)

def init_app(app: Flask):

    bp_api.register_blueprint(users_routes.bp)

    app.register_blueprint(bp_api)