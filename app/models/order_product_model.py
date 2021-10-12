from sqlalchemy.orm import relationship
from app.configs.database import db
from sqlalchemy import Column, Integer, ForeignKey
from app.services.helper import DefaultModel
from dataclasses import field, dataclass

@dataclass
class OrderProductModel(db.Model, DefaultModel):
    quantity: int
    total_value: int
    product: dict = field(default_factory=dict)
    __tablename__ = 'orders_product'

    orders_product_id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey('orders.order_id'))
    product_id = Column(Integer, ForeignKey('products.product_id'))
    quantity = Column(Integer, nullable=False)
    total_value = Column(Integer, nullable=False)

    product = relationship('ProductModel', backref='order_product')