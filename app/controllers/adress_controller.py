from flask import request, jsonify
from app.models.adresses_model import AdressModel
from flask_jwt_extended import (
    jwt_required,
    get_current_user
)
from http import HTTPStatus

@jwt_required()
def create_adress():
    data_json = request.get_json()

    user = get_current_user()
    adress = AdressModel(**data_json)
    user.adresses.append(adress)

    adress.save_self()
    
    return jsonify(adress), HTTPStatus.CREATED


@jwt_required()
def read_adress():
    user = get_current_user()

    return jsonify(user.adresses), HTTPStatus.OK

@jwt_required()
def update_adress(adress_id):
    adress = AdressModel.query.get(adress_id)
    update_data = request.get_json()

    # TODO -> Verificação se o user do token é o 
    # proprietario do adress sendo atualizado

    for key, value in update_data.items():
        setattr(adress, key, value)

    adress.save_self()

    return jsonify(adress), HTTPStatus.OK

@jwt_required()
def delete_adress(adress_id):
    adress = AdressModel.query.get(adress_id)

    adress.delete_self()

    return '', HTTPStatus.NO_CONTENT
