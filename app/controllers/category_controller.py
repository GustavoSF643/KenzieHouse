from dataclasses import asdict

import sqlalchemy
from app.exceptions.category_exc import InvalidKeysError, InvalidTypeError
from app.models.category_model import CategoryModel
from app.services.admin_verify import admin_verify
from environs import Env
from flask import jsonify, request
from flask_jwt_extended.view_decorators import jwt_required

env = Env()
env.read_env()

# @jwt_required()
# @admin_verify
def create_category():
    try:
        category_data = request.json

        category = CategoryModel(**category_data)
        category.save_self()

        return jsonify(category), 201
    except TypeError:
        return jsonify(error='invalid keys in json-body'), 406
    except sqlalchemy.exc.IntegrityError:
        return jsonify(error='Category already exists.'), 409
    except InvalidTypeError as e:
        return jsonify(error=str(e)), 406


def get_categories():
    name = request.args.get('name')

    if name:
        categories = CategoryModel.query.where(sqlalchemy.text(f"categories.name ~ '{name}'")).all()
    else:
        categories = CategoryModel.query.all()

    output_categories = []
    for category in categories:
        category_dict = asdict(category)

        host = env('HOST')
        category_dict['products'] = f"{host}/categories/{category_dict['category_id']}/products"
        
        output_categories.append(category_dict)

    return jsonify(output_categories), 200


def get_category_by_id(id: int):
    category = CategoryModel.query.get(id)

    if not category:
        return jsonify(error='Category not found.'), 404

    return jsonify(category), 200


def get_products_by_category_id(category_id: int):
    category_products = CategoryModel.query.get(category_id).products

    return jsonify(category_products), 200


# @jwt_required()
# @admin_verify
def update_category_by_id(id: int):
    try:
        category_data = request.json

        category:CategoryModel = CategoryModel.query.get(id)

        if not category:
            return jsonify(error='Category not found.'), 404

        category.update(category_data)

        return jsonify(category), 200
    except (InvalidKeysError, InvalidTypeError) as e:
        return jsonify(error=str(e)), 406


# @jwt_required()
# @admin_verify
def delete_category_by_id(id: int):
    category:CategoryModel = CategoryModel.query.get(id)
    
    if not category:
        return jsonify(error='Category not found.'), 404

    category.delete_self()

    return {}, 204
