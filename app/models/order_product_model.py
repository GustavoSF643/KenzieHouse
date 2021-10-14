from sqlalchemy.orm import relationship, validates
from app.configs.database import db
from sqlalchemy import Column, Integer, ForeignKey
from app.services.helper import DefaultModel
from dataclasses import field, dataclass
from app.exceptions.order_exc import InvalidTypeError

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

    @validates('quantity', 'total_value')
    def validate_int_type(self, key, value):
        if type(value) is not int:
            raise InvalidTypeError(f'{key} must be a int type.')
        
        return value
