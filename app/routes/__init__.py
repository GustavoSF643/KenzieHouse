from flask import Flask, Blueprint
from . import (
    users_routes, 
    adresses_routes,
    categories_routes
)

bp_api = Blueprint('api_bp', __name__)

def init_app(app: Flask):

    bp_api.register_blueprint(users_routes.bp)
    bp_api.register_blueprint(adresses_routes.bp)
    bp_api.register_blueprint(categories_routes.bp)

    app.register_blueprint(bp_api)