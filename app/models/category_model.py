from dataclasses import dataclass

from app.configs.database import db
from app.exceptions.category_exc import InvalidKeysError, InvalidTypeError
from app.services.helper import DefaultModel
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import validates


@dataclass
class CategoryModel(db.Model, DefaultModel):

    category_id: int
    name: str
    description: str

    __tablename__ = 'categories'

    category_id = Column(Integer, primary_key=True)
    name = Column(String(127), nullable=False, unique=True)
    description = Column(String(255))

    @validates('name')
    def validate_phone(self, key, name):
        if type(name) != str:
            raise InvalidTypeError('Name must be a string type.')

        return name

    @validates('description')
    def validate_phone(self, key, name):
        if type(name) != str:
            raise InvalidTypeError('Description must be a string type.')

        return name


    def update(self, data):
        try:
            CategoryModel(**data)
        except TypeError:
            keys = ('name', 'description')
            raise InvalidKeysError(f"Invalid Keys in body. Accepted Keys:{', '.join(keys)}")

        for key, value in data.items():
            setattr(self, key, value)
