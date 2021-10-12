from flask import request, jsonify
from app.models.adress_model import AdressModel
from flask_jwt_extended import (
    jwt_required,
    get_current_user
)
from http import HTTPStatus
from app.exceptions.adress_exc import (
    AdressNotFound, 
    InvalidTypeError, 
    UnauthorizedUserAcess, 
    InvalidKeysError
)

@jwt_required()
def create_adress():
    data_json = request.get_json()

    user = get_current_user()

    try:
        AdressModel.validate_keys(data_json, create=True)
        adress = AdressModel(**data_json)
        user.adresses.append(adress)

        adress.save_self()

    except InvalidTypeError as e:
        return jsonify(error=str(e)), HTTPStatus.BAD_REQUEST

    except InvalidKeysError as e:
        return jsonify(error=str(e)), HTTPStatus.BAD_REQUEST

    return jsonify(adress), HTTPStatus.CREATED


@jwt_required()
def read_adress():
    user = get_current_user()

    return jsonify(user.adresses), HTTPStatus.OK

@jwt_required()
def update_adress(adress_id):
    user = get_current_user()

    try:
        adress = AdressModel.adress_verify(adress_id)
        adress.user_adress_verify(user.user_id)
        update_data = request.get_json()

        adress.update(update_data)
    
    except AdressNotFound as e:
        return jsonify(error=str(e)), HTTPStatus.NOT_FOUND

    except UnauthorizedUserAcess as e:
        return jsonify(error=str(e)), HTTPStatus.UNAUTHORIZED

    except InvalidKeysError as e:
        return jsonify(error=str(e)), HTTPStatus.BAD_REQUEST

    return jsonify(adress), HTTPStatus.OK

@jwt_required()
def delete_adress(adress_id):
    user = get_current_user()

    try:
        adress = AdressModel.adress_verify(adress_id)
        adress.user_adress_verify(user.user_id)

        adress.delete_self()

    except AdressNotFound as e:
        return jsonify(error=str(e)), HTTPStatus.NOT_FOUND  

    except UnauthorizedUserAcess as e:
        return jsonify(error=str(e)), HTTPStatus.UNAUTHORIZED  
    
    return '', HTTPStatus.NO_CONTENT
