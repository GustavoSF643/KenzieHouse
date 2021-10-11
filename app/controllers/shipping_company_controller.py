import sqlalchemy
from app.exceptions.shipping_company_exc import InvalidKeysError, InvalidTypeError
from app.models.shipping_company_model import ShippingCompanyModel
from flask import jsonify, request
from flask_jwt_extended import jwt_required


# @jwt_required()
def create_shipping_company():
    try:
        shipping_company_data = request.json

        shipping_company = ShippingCompanyModel(**shipping_company_data)
        
        shipping_company.save_self()

        return jsonify(shipping_company), 201
    except TypeError:
        return jsonify(error='invalid keys in json-body'), 406
    except sqlalchemy.exc.IntegrityError:
        return jsonify(error='cnpj already exists.'), 409
    except InvalidTypeError as e:
        return jsonify(error=str(e)), 406  

# @jwt_required()
def get_shipping_company():
    shipping_company = ShippingCompanyModel.query.all()

    return jsonify(shipping_company), 200

# @jwt_required()
def get_shipping_company_by_id(id: int):
    shipping_company: ShippingCompanyModel = ShippingCompanyModel.query.get(id)

    if not shipping_company:
        return jsonify(error='Shipping Company not found.'), 404

    return jsonify(shipping_company), 200

# @jwt_required()
def update_shipping_company_by_id(id: int):
    try:
        shipping_company_data = request.json

        shipping_company:ShippingCompanyModel = ShippingCompanyModel.query.get(id)

        if not shipping_company:
            return jsonify(error='Shipping Company not found.'), 404

        shipping_company.update(shipping_company_data)

        return jsonify(shipping_company), 200
    except (InvalidKeysError, InvalidTypeError) as e:
        return jsonify(error=str(e)), 406

# @jwt_required()
def delete_shipping_company_by_id(id: int):
    shipping_company:ShippingCompanyModel = ShippingCompanyModel.query.get(id)
    
    if not shipping_company:
        return jsonify(error='Shipping Company not found.'), 404
    shipping_company.delete_self()

    return {}, 204
