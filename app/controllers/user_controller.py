from http import HTTPStatus

import sqlalchemy
from app.exceptions.user_exc import (InvalidCellphoneFormatError,
                                     InvalidCpfFormatError, InvalidKeysError,
                                     InvalidTypeError, WrongPasswordError)
from app.models.user_model import UserModel
from flask import jsonify, request
from flask_jwt_extended import (create_access_token, create_refresh_token,
                                get_current_user, get_jwt_identity,
                                jwt_required)


def create_user():
    try:
        data_json = request.get_json()
        password_to_hash = data_json.pop('password')
        if 'admin' in data_json:
            data_json.pop('admin')

        user = UserModel(**data_json)
        user.password = password_to_hash

        user.save_self()

        return jsonify(user), HTTPStatus.CREATED
    except TypeError:
        return jsonify(error='invalid keys in json-body'), 406
    except sqlalchemy.exc.IntegrityError as e:
        error_str = str(e.orig).split('\n')[1].replace('DETAIL:  Key ', '')
        return jsonify(error=error_str), 409
    except (
        InvalidTypeError, InvalidCellphoneFormatError, InvalidCpfFormatError
    ) as e:
        return jsonify(error=str(e)), 406


def login_user():
    try:
        email = request.json['email']
        password = request.json['password']

        user: UserModel = UserModel.query.filter_by(email=email).one()

        user.validate_password(password)

        access_token = create_access_token(identity=user)
        refresh_token = create_refresh_token(identity=user)

        return jsonify(
            acces_token=access_token, 
            refresh_token=refresh_token
        ), 200
    except WrongPasswordError as e:
        return jsonify(error=str(e)), 403
    except sqlalchemy.exc.NoResultFound:
        return {'message': 'User not found'}, 404
    except KeyError:
        return {'message':
                'Keys not acceptable. Valid keys: (email, password).'}, 406


@jwt_required()
def read_user():
    return get_jwt_identity(), HTTPStatus.OK


@jwt_required()
def update_user():
    try:
        user: UserModel = get_current_user()
        update_data = request.get_json()

        user.update(update_data)

        return jsonify(user), HTTPStatus.OK
    except (InvalidKeysError, InvalidTypeError) as e:
        return jsonify(error=str(e)), 406


@jwt_required()
def delete_user():
    user: UserModel = get_current_user()

    user.delete_self()

    return '', HTTPStatus.NO_CONTENT


@jwt_required(refresh=True)
def refresh_jwt_token():
    identity = get_jwt_identity()
    access_token = create_access_token(identity=identity)

    return jsonify(access_token=access_token)
