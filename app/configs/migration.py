from flask import Flask
from flask_migrate import Migrate

def init_app(app: Flask):
    # Aqui vem os import de models
    from app.models.user_model import UserModel
    from app.models.adress_model import AdressModel

    Migrate(app, app.db, compare_type=True)
