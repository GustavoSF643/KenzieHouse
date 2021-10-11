from dataclasses import dataclass

from app.configs.database import db
from app.exceptions.product_exc import InvalidKeysError, InvalidTypeError
from app.services.helper import DefaultModel
from sqlalchemy import Column, Float, ForeignKey, Integer, String
from sqlalchemy.orm import validates


@dataclass
class ProductModel(db.Model, DefaultModel):

    name: str
    description: str
    rate: str
    weight: str
    height: str
    length: str
    width: str
    price: int
    discount_value: int
    stock_quantity: int

    __tablename__ = 'products'

    product_id = Column(Integer, primary_key=True)
    category_id = Column(Integer, ForeignKey('categories.category_id'), nullable=False)
    name = Column(String(127), nullable=False)
    description = Column(String(511))
    rate = Column(Float)
    weight = Column(String(16))
    height = Column(String(16))
    length = Column(String(16))
    width = Column(String(16))
    price = Column(Integer, nullable=False)
    discount_value = Column(Integer, nullable=False)
    stock_quantity = Column(Integer, nullable=False)

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