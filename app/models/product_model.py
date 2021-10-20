import os
import secrets
from dataclasses import dataclass

from app.configs.database import db
from app.exceptions.product_exc import (InvalidKeysError, InvalidTypeError,
                                        ProductNotFound)
from app.models.product_image_model import ProductImageModel
from app.services.helper import DefaultModel
from environs import Env
from flask import safe_join
from sqlalchemy import Column, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship, validates
from werkzeug.datastructures import FileStorage

env = Env()
env.read_env()


@dataclass
class ProductModel(db.Model, DefaultModel):

    product_id: int
    name: str
    description: str
    rate: float
    weight: str
    height: str
    length: str
    width: str
    price: int
    discount_value: int
    stock_quantity: int
    category: dict
    image: dict

    __tablename__ = 'products'

    product_id = Column(Integer, primary_key=True)
    category_id = Column(Integer, ForeignKey('categories.category_id'), nullable=False)
    name = Column(String(127), nullable=False)
    description = Column(String(511))
    rate = Column(Float)
    weight = Column(String(16), nullable=False)
    height = Column(String(16), nullable=False)
    length = Column(String(16), nullable=False)
    width = Column(String(16), nullable=False)
    price = Column(Integer, nullable=False)
    discount_value = Column(Integer, nullable=False)
    stock_quantity = Column(Integer, nullable=False)

    category = relationship('CategoryModel', backref='products')
    image = relationship('ProductImageModel', backref='product', uselist=False)

    @validates('name', 'description', 'weight', 'height', 'length', 'width')
    def validate_string_type(self, key, value):
        if type(value) != str:
            raise InvalidTypeError(f'{key} must be a string type.')

        return value

    @validates('rate')
    def validate_rate_type(self, key, value):
        if type(value) != float:
            raise InvalidTypeError(f'{key} must be a float type.')

        return value

    @validates('price', 'discount_value', 'stock_quantity')
    def validate_integer_type(self, key, value):
        if type(value) != int:
            raise InvalidTypeError(f'{key} must be a integer type.')

        return value

    def update(self, data):
        try:
            ProductModel(**data)
        except TypeError:
            keys = (
                'name', 'description', 'weight', 'height', 'length', 'width', 'rate', 'price', 'discount_value', 'stock_quantity'
            )
            raise InvalidKeysError(f"Invalid Keys in body. Accepted Keys:{', '.join(keys)}")

        for key, value in data.items():
            setattr(self, key, value)
            
        self.save_self()

    @staticmethod
    def product_verify(product_id):
        product: ProductModel = ProductModel.query.get(product_id)

        if not product:
            raise ProductNotFound('Product not found.')

        return product


    def save_product_img(self, image: FileStorage):
        if self.image:
            product_image = ProductImageModel.query.get(self.image.product_image_id)
            product_image.delete_self()
            
            product_image_folder = env('PRODUCT_IMAGE_FOLDER')
            image_type = '.' + product_image.type.split('/')[1]
            image_filename = product_image.image_filename + image_type
            image_path = safe_join(product_image_folder, image_filename)
            try:
                os.remove(image_path)
            except FileNotFoundError:
                ...

        filename = str(secrets.token_urlsafe(16))
        file_type = '.' + image.mimetype.split('/')[1]
        product_image_folder = env('PRODUCT_IMAGE_FOLDER')
        file_path = safe_join(product_image_folder, filename + file_type)

        image.save(file_path)

        host = env('HOST')

        product_image_dict = {
            'product_id': self.product_id,
            'name': image.filename,
            'link': f"/products/{self.product_id}/{filename}",
            'type': image.mimetype,
            'image_filename': filename
        }

        product_image: ProductImageModel = ProductImageModel(**product_image_dict)
        product_image.save_self()

        return filename
