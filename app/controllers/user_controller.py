from flask import request, jsonify
from app.models.user_model import UserModel
from flask_jwt_extended import (
    jwt_required,
    create_access_token,
    create_refresh_token,
    get_jwt_identity,
    get_current_user
)
from http import HTTPStatus

def create_user():
    data_json = request.get_json()
    password_to_hash = data_json.pop('password')

    user = UserModel(**data_json)
    user.password = password_to_hash

    user.save_self()
    
    return jsonify(user), HTTPStatus.CREATED

def login_user():
    email = request.json.get('email')
    password = request.json.get('password')

    user = UserModel.query.filter_by(email=email).first()
    
    if user.validate_password(password):
        access_token = create_access_token(identity=user)
        refresh_token = create_refresh_token(identity=user)

        return jsonify(
            acces_token=access_token, 
            refresh_token=refresh_token
        ), HTTPStatus.OK


@jwt_required()
def read_user():
    return get_jwt_identity(), HTTPStatus.OK

@jwt_required()
def update_user():
    user = get_current_user()
    update_data = request.get_json()

    for key, value in update_data.items():
        setattr(user, key, value)

    user.update()
    user.save_self()

    return jsonify(user), HTTPStatus.OK

@jwt_required()
def delete_user():
    user = get_current_user()

    user.delete_self()

    return '', HTTPStatus.NO_CONTENT

@jwt_required(refresh=True)
def refresh_jwt_token():
    identity = get_jwt_identity()
    access_token = create_access_token(identity=identity)

    return jsonify(access_token=access_token)