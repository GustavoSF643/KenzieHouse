from flask import Flask
from app.configs import database, migration, environment, jwt
from app import routes

def create_app():

    app = Flask(__name__)

    environment.init_app(app)
    jwt.init_app(app)
    database.init_app(app)
    migration.init_app(app)
    routes.init_app(app)

    return app