import sqlalchemy
from app.exceptions.category_exc import CategoryNotFoundError
from app.exceptions.product_exc import (InvalidKeysError, InvalidLinkError,
                                        InvalidTypeError)
from app.models.category_model import CategoryModel
from app.models.product_image_model import ProductImageModel
from app.models.product_model import ProductModel
from environs import Env
from flask import jsonify, request
from flask_cors import cross_origin
from flask_jwt_extended import jwt_required

env = Env()
env.read_env()

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


@cross_origin()
def upload_product_image_by_product_id(product_id: int):
    files = request.files
    files_name = list(files)
    image = files[files_name[0]]

    product: ProductModel = ProductModel.query.get(product_id)
    product.save_product_img(image)

    return jsonify(product), 200
        


def get_image_product(product_id, image_name):
    try:
        product: ProductModel = ProductModel.query.get(product_id)

        product_image = product.image

        product_image: ProductImageModel = product_image

        return product_image.download_image(image_name)
    except AttributeError:
        return jsonify(error='Image not found'), 404
    except InvalidLinkError as e:
        return jsonify(error=str(e)), 400


def get_products():
    name = request.args.get('name')

    if name:
        products = ProductModel.query.where(sqlalchemy.text(f"products.name ~ '{name}'")).all()
    else:
        products = ProductModel.query.all()

    return_products = []
    for product in products:
        host = env('HOST')

        formated_product = {
            "product_id": product.product_id,
            "name": product.name,
            "description": product.description,
            "category": product.category.name,
            "image": product.image,
            "product_info": f"{host}/products/{product.product_id}"
        }
        return_products.append(formated_product)

    return jsonify(return_products), 200


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
