from dataclasses import dataclass

from app.configs.database import db
from app.services.helper import DefaultModel
from sqlalchemy import Column, Integer, String


@dataclass
class CategoryModel(db.Model, DefaultModel):

    name: str
    description: str

    __tablename__ = 'categories'

    category_id = Column(Integer, primary_key=True)
    name = Column(String(127), nullable=False, unique=True)
    description = Column(String(255))
