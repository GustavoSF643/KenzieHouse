from app.configs.database import db
from app.services.helper import DefaultModel
from sqlalchemy import Column, Integer, String, ForeignKey
from dataclasses import dataclass
from app.exceptions.adress_exc import AdressNotFound, InvalidTypeError, UnauthorizedUserAcess, InvalidKeysError
from sqlalchemy.orm import validates

@dataclass
class AdressModel(db.Model, DefaultModel):
    adress_id: int
    street: str
    house_number: int
    district: str
    city: str
    state: str
    cep: str
    __tablename__ = 'adresses'

    adress_id = Column(Integer, primary_key=True)
    street = Column(String(100), nullable=False)
    house_number = Column(Integer, nullable=False)
    district = Column(String(50), nullable=False)
    city = Column(String(50), nullable=False)
    state = Column(String(50), nullable=False)
    cep = Column(String(50), nullable=False)

    user_id = Column(Integer, ForeignKey('users.user_id'))

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
    def validate_keys(data, create=False):
        valid_keys = ['street', 'house_number', 'district', 'city', 'state', 'cep']

        if create:
            valid_keys.sort()
            if sorted(list(data.keys())) != valid_keys:
                raise InvalidKeysError('Required key/s are missing.')

        for key in data.keys():
            if key not in valid_keys:
                raise InvalidKeysError(f"Invalid Keys in body. Accepted Key: {', '.join(valid_keys)}")

    def update(self, data):
        AdressModel.validate_keys(data)

        for key, value in data.items():
            setattr(self, key, value)

        self.save_self()

    @staticmethod
    def adress_verify(adrees_id):
        adress: AdressModel = AdressModel.query.get(adrees_id)

        if not adress:
            raise AdressNotFound('Adress not found.')

        return adress

    def user_adress_verify(self, user_id):
        if user_id != self.user.user_id:
            raise UnauthorizedUserAcess('Adress not belongs to this user.')
