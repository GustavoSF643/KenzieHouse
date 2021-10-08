from flask import Flask
from flask_migrate import Migrate

def init_app(app: Flask):
    # Aqui vem os import de models

    Migrate(app, app.db)
