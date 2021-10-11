from flask import Flask
from flask_jwt_extended import JWTManager
from app.models.user_model import UserModel

jwt = JWTManager()

def init_app(app: Flask):
    jwt.init_app(app)

    @jwt.user_lookup_loader
    def current_user_model(_, jwt_data):
        user_email = jwt_data['sub']['email']
        user = UserModel.query.filter_by(email=user_email).first()

        return user
