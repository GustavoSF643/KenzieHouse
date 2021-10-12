from dataclasses import dataclass

from app.configs.database import db
from app.exceptions.payment_exc import InvalidKeysError, InvalidTypeError, PaymentMethodNotFound
from app.services.helper import DefaultModel
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import validates


@dataclass
class PaymentMethodModel(db.Model, DefaultModel):

    payment_method_id: int
    name: str
    description: str

    __tablename__ = 'payment_methods'

    payment_method_id = Column(Integer, primary_key=True)
    name = Column(String(127), nullable=False, unique=True)
    description = Column(String(255))

    @validates('name', 'description')
    def validate_string_type(self, key, value):
        if type(value) != str:
            raise InvalidTypeError(f'{key} must be a string type.')

        return value


    def update(self, data):
        try:
            PaymentMethodModel(**data)
        except TypeError:
            keys = ('name', 'description')
            raise InvalidKeysError(f"Invalid Keys in body. Accepted Keys:{', '.join(keys)}")

        for key, value in data.items():
            setattr(self, key, value)
            
        self.save_self()

    @staticmethod
    def payment_method_verify(payment_method_id):
        payment_method: PaymentMethodModel = PaymentMethodModel.query.get(payment_method_id)

        if not payment_method:
            raise PaymentMethodNotFound('Payment method not found.')

        return payment_method