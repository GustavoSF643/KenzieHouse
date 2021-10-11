from flask import request, jsonify
import sqlalchemy
from app.exceptions.category_exc import InvalidTypeError
from app.models.category_model import CategoryModel

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
    categories = CategoryModel.query.all()

    return jsonify(categories), 200


def get_category_by_id(id: int):
    category = CategoryModel.query.get(id)

    if not category:
        return jsonify(error='Category not found.'), 404

    return jsonify(category), 200


def update_category_by_id(id: int):
    category_data = request.json

    category:CategoryModel = CategoryModel.query.get(id)

    if not category:
        return jsonify(error='Category not found.'), 404

    category.update(category_data)

    return jsonify(category), 200


def delete_category_by_id(id: int):
    category:CategoryModel = CategoryModel.query.get(id)
    
    if not category:
        return jsonify(error='Category not found.'), 404

    category.delete_self()

    return {}, 204