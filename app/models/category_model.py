from dataclasses import dataclass

from app.configs.database import db
from app.exceptions.category_exc import CategoryNotFoundError, InvalidKeysError, InvalidTypeError
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

    @validates('name', 'description')
    def validate_string_type(self, key, value):
        if type(value) != str:
            raise InvalidTypeError(f'{key} must be a string type.')

        return value


    def update(self, data):
        try:
            CategoryModel(**data)
        except TypeError:
            keys = ('name', 'description')
            raise InvalidKeysError(f"Invalid Keys in body. Accepted Keys:{', '.join(keys)}")

        for key, value in data.items():
            setattr(self, key, value)

        self.save_self()

    @staticmethod
    def category_verify(category_name: str):
        category:CategoryModel = CategoryModel.query.filter_by(name=category_name).first()

        if not category:
            raise CategoryNotFoundError('Category not found.')

        return category.category_id