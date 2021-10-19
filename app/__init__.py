from flask import Flask
from app.configs import database, migration, environment, jwt
from app import routes
import os
from environs import Env
from flask_cors import CORS

env = Env()
env.read_env()

if not os.path.exists(f"./{env('PRODUCT_IMAGE_FOLDER')}"):
    os.makedirs(f"./{env('PRODUCT_IMAGE_FOLDER')}")

def create_app():

    app = Flask(__name__)
    CORS(app, origins=[env('FRONTEND_APP')])

    environment.init_app(app)
    jwt.init_app(app)
    database.init_app(app)
    migration.init_app(app)
    routes.init_app(app)

    return app
