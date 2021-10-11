from dataclasses import dataclass

from app.configs.database import db
from app.services.helper import DefaultModel
from sqlalchemy import Column, String, Integer, Float, ForeignKey


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

