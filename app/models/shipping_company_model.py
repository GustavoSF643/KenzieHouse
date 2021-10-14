from dataclasses import dataclass
import re
from app.configs.database import db
from app.exceptions.shipping_company_exc import InvalidKeysError, InvalidTypeError, ShippingCompanyNotFound, InvalidCnpjFormatError
from app.services.helper import DefaultModel
from sqlalchemy import Column, Float, Integer, String
from sqlalchemy.orm import validates


@dataclass
class ShippingCompanyModel(db.Model, DefaultModel):

    name: str
    cnpj: str
    rate: str
   

    __tablename__ = 'shipping_companies'

    shipping_company_id = Column(Integer, primary_key=True)
    name = Column(String(127), nullable=False)
    cnpj = Column(String(100), nullable=False, unique=True)
    rate = Column(Float)


    @validates('name')
    def validate_string_type(self, key, value):
        if type(value) != str:
            raise InvalidTypeError(f'{key} must be a string type.')

        return value

    @validates('cnpj')
    def validate_cnpj_pattern(self, key, value):
        if type(value) != str:
            raise InvalidTypeError(f'{key} must be a string type.')

        string = value
        pattern = '\d{2}\.\d{3}\.\d{3}\/\d{4}\-\d{2}'

        if not re.fullmatch(pattern, string):
            raise InvalidCnpjFormatError("Invalid cnpj format. Valid format: '00.000.000/0000-00'")

        return value

    @validates('rate')
    def validate_rate_type(self, key, value):
        if type(value) != float:
            raise InvalidTypeError(f'{key} must be a float type.')

        return value

    def update(self, data):
        try:
            ShippingCompanyModel(**data)
        except TypeError:
            keys = ('name', 'cnpj', 'rate')
            raise InvalidKeysError(f"Invalid Keys in body. Accepted Keys:{', '.join(keys)}")

        for key, value in data.items():
            setattr(self, key, value)
            
        self.save_self()

    @staticmethod
    def shipping_company_verify(shipping_company_id):
        shipping_company: ShippingCompanyModel = ShippingCompanyModel.query.get(shipping_company_id)

        if not shipping_company:
            raise ShippingCompanyNotFound('Shipping company not found.')

        return shipping_company
