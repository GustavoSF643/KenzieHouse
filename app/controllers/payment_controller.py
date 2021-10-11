import sqlalchemy
from app.exceptions.payment_exc import InvalidKeysError, InvalidTypeError
from app.models.payment_method_model import PaymentMethodModel
from flask import jsonify, request
from flask_jwt_extended import jwt_required


@jwt_required()
def create_payment():
    try:
        payment_data = request.json

        payment = PaymentMethodModel(**payment_data)
        payment.save_self()

        return jsonify(payment), 201
    except TypeError:
        return jsonify(error='Invalid keys in json-body'), 406
    except sqlalchemy.exc.IntegrityError:
        return jsonify(error='Payment method already exists.'), 409
    except InvalidTypeError as e:
        return jsonify(error=str(e)), 406


@jwt_required()
def get_payments():
    payments = PaymentMethodModel.query.all()

    return jsonify(payments), 200


@jwt_required()
def get_payment_by_id(id: int):
    payment: PaymentMethodModel = PaymentMethodModel.query.get(id)

    if not payment:
        return jsonify(error='Payment method not found.'), 404

    return jsonify(payment), 200


@jwt_required()
def update_payment_by_id(id: int):
    try:
        payment_data = request.json

        payment:PaymentMethodModel = PaymentMethodModel.query.get(id)

        if not payment:
            return jsonify(error='Payment method not found.'), 404

        payment.update(payment_data)

        return jsonify(payment), 200
    except (InvalidKeysError, InvalidTypeError) as e:
        return jsonify(error=str(e)), 406


@jwt_required()
def delete_payment_by_id(id: int):
    payment:PaymentMethodModel = PaymentMethodModel.query.get(id)
    
    if not payment:
        return jsonify(error='Payment method not found.'), 404

    payment.delete_self()

    return {}, 204
