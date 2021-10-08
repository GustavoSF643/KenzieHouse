from flask import Flask, Blueprint

bp_api = Blueprint('api_bp', __name__)

def init_app(app: Flask):

    app.register_blueprint(bp_api)