from sqlalchemy.orm import relationship, validates
from app.configs.database import db
from app.services.helper import DefaultModel
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from dataclasses import dataclass, field
from datetime import datetime
from app.exceptions.order_exc import InvalidTypeError, InvalidKeysError, UnauthorizedUserAcess, OrderNotFound

@dataclass
class OrderModel(db.Model, DefaultModel):
    status: str
    created_at: datetime
    user: dict = field(default_factory=dict)
    shipping_company: dict  = field(default_factory=dict)
    adress: dict  = field(default_factory=dict)
    payment_method: dict  = field(default_factory=dict)
    orders_product: list = field(default_factory=list)
    __tablename__ = 'orders'

    order_id = Column(Integer, primary_key=True)
    status = Column(String, nullable=False, default='Aguardando Pagamento')
    created_at = Column(DateTime, default=datetime.utcnow())

    user_id = Column(Integer, ForeignKey('users.user_id'))
    adress_id = Column(Integer, ForeignKey('orders_adresses.order_adress_id'))
    shipping_company_id = Column(Integer, ForeignKey('shipping_companies.shipping_company_id'))
    payment_method_id = Column(Integer, ForeignKey('payment_methods.payment_method_id'))

    shipping_company = relationship('ShippingCompanyModel', backref='orders')
    adress = relationship('OrderAdressModel', backref='orders')
    payment_method = relationship('PaymentMethodModel', backref='orders')
    orders_product = relationship('OrderProductModel', backref='order')

    @validates('status')
    def validate_string_type(self, key, value):
        if type(value) is not str:
            raise InvalidTypeError(f'{key} must be a string type.')

        return value

    def update(self, data):
        valid_key = ['status']

        if list(data.keys()) != valid_key:
            raise InvalidKeysError(f"Invalid Keys in body. Accepted Key: {', '.join(valid_key)}")

        self.status = data['status']
        self.save_self()

    def user_order_verify(self, user_id):
        if user_id != self.user.user_id:
            raise UnauthorizedUserAcess('Order not belongs to this user.')

    @staticmethod
    def order_verify(order_id):
        order: OrderModel = OrderModel.query.get(order_id)

        if not order:
            raise OrderNotFound('Order not found.')

        return order
