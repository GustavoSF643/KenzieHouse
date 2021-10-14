import sqlalchemy
from app.exceptions.category_exc import CategoryNotFoundError
from app.exceptions.product_exc import InvalidKeysError, InvalidTypeError
from app.models.category_model import CategoryModel
from app.models.product_model import ProductModel
from flask import jsonify, request
from flask_jwt_extended import jwt_required


@jwt_required()
def create_product():
    try:
        product_data = request.json

        category_name = product_data.pop('category')
        product_data['category_id'] = CategoryModel.category_verify(category_name)

        product = ProductModel(**product_data)
        product.save_self()

        return jsonify(product), 201
    except TypeError:
        return jsonify(error='invalid keys in json-body'), 406
    except sqlalchemy.exc.IntegrityError:
        return jsonify(error='Product already exists.'), 409
    except InvalidTypeError as e:
        return jsonify(error=str(e)), 406  
    except CategoryNotFoundError as e:
        return jsonify(error=str(e)), 404  

def get_products():
    name = request.args.get('name')
     
    if name:
        products = ProductModel.query.where(sqlalchemy.text(f"products.name ~ '{name}'")).all()
    else:
        products = ProductModel.query.all()

    return jsonify(products), 200


def get_product_by_id(id: int):
    product: ProductModel = ProductModel.query.get(id)

    if not product:
        return jsonify(error='Product not found.'), 404

    return jsonify(product), 200


@jwt_required()
def update_product_by_id(id: int):
    try:
        product_data = request.json

        product:ProductModel = ProductModel.query.get(id)

        if not product:
            return jsonify(error='Product not found.'), 404

        product.update(product_data)

        return jsonify(product), 200
    except (InvalidKeysError, InvalidTypeError) as e:
        return jsonify(error=str(e)), 406


@jwt_required()
def delete_product_by_id(id: int):
    product:ProductModel = ProductModel.query.get(id)
    
    if not product:
        return jsonify(error='Product not found.'), 404

    product.delete_self()

    return {}, 204
