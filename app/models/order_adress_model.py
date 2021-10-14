from app.configs.database import db
from app.services.helper import DefaultModel
from sqlalchemy import Column, Integer, String
from dataclasses import dataclass
from app.exceptions.adress_exc import InvalidTypeError
from sqlalchemy.orm import validates

@dataclass
class OrderAdressModel(db.Model, DefaultModel):
    street: str
    house_number: int
    district: str
    city: str
    state: str
    cep: str
    __tablename__ = 'orders_adresses'

    order_adress_id = Column(Integer, primary_key=True)
    street = Column(String(100), nullable=False)
    house_number = Column(Integer, nullable=False)
    district = Column(String(50), nullable=False)
    city = Column(String(50), nullable=False)
    state = Column(String(50), nullable=False)
    cep = Column(String(50), nullable=False)

    @validates('street', 'district', 'city', 'state', 'cep')
    def validate_str_type(self, key, value):
        if type(value) is not str:
            raise InvalidTypeError(f'{key} must be a string type.')

        return value

    @validates('house_number')
    def validate_int_type(self, key, value):
        if type(value) is not int:
            raise InvalidTypeError(f'{key} must be a int type')

        return value

    @staticmethod
    def order_adress_verify(data):
        adress: OrderAdressModel = OrderAdressModel.query.filter_by(
            street=data['street'],
            house_number=data['house_number'],
            district=data['district'],
            city=data['city'],
            state=data['state'],
            cep=data['cep']
        ).first()

        if not adress:
            adress = OrderAdressModel(**data)
            adress.save_self() 

            return adress
        
        return adress