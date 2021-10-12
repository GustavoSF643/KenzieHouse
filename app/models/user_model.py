import re
from app.configs.database import db
from app.exceptions.user_exc import InvalidCellphoneFormatError, InvalidCpfFormatError, InvalidKeysError, InvalidTypeError, WrongPasswordError
from app.services.helper import DefaultModel
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash, check_password_hash
from dataclasses import dataclass
from datetime import datetime
from sqlalchemy.orm import validates


@dataclass
class UserModel(db.Model, DefaultModel):
    name: str
    last_name: str
    email: str
    genre: str
    birthdate: str

    __tablename__ = 'users'

    user_id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False) 
    last_name = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False, unique=True)
    cpf = Column(String(100), nullable=False, unique=True)
    genre = Column(String(15))
    birthdate = Column(DateTime, nullable=False)
    cellphone = Column(String(100), nullable=False, unique=True)
    created_at = Column(DateTime, default=datetime.utcnow())
    updated_at = Column(DateTime, default=datetime.utcnow())
    password_hash = Column(String, nullable=False)

    adresses = relationship('AdressModel', backref='user')
    orders = relationship('OrderModel', backref='user')

    @validates('name', 'last_name', 'genre')
    def validate_string_type(self, key, value):
        if type(value) != str:
            raise InvalidTypeError(f'{key} must be a string type.')

        return value

    @validates('email')
    def validate_email(self, key, value):
        if type(value) != str:
            raise InvalidTypeError(f'{key} must be a string type.')

        string = value
        pattern = '^([\w\.\-]+)@([\w\-]+)((\.(\w){2,3})+)$'

        if not re.fullmatch(pattern, string):
            raise InvalidCpfFormatError("Invalid email format. Valid format: 'example@example.com'")

        return value

    @validates('cpf')
    def validate_cpf(self, key, value):
        if type(value) != str:
            raise InvalidTypeError(f'{key} must be a string type.')

        string = value
        pattern = '[0-9]{3}\.?[0-9]{3}\.?[0-9]{3}\-?[0-9]{2}'

        if not re.fullmatch(pattern, string):
            raise InvalidCpfFormatError("Invalid cpf format. Valid format: '000.000.000-00'")

        return value

    @validates('cellphone')
    def validate_cellphone(self, key, value):
        if type(value) != str:
            raise InvalidTypeError(f'{key} must be a string type.')

        string = value
        pattern = '\(\d{2}\)\s\d{4,5}\-\d{4}'

        if not re.fullmatch(pattern, string):
            raise InvalidCellphoneFormatError("Invalid cellphone format. Valid formats: '(00) 01234-5678', '(00) 1234-5678'")

        return value

    @property
    def password(self):
        raise AttributeError("Password cannot be accessed!")

    @password.setter
    def password(self, password_to_hash):
        self.password_hash = generate_password_hash(password_to_hash)

    def validate_password(self, password_to_validate):
        if not check_password_hash(self.password_hash, password_to_validate):
            raise WrongPasswordError('Password is wrong.')

    def update(self, data):
        self.updated_at = datetime.utcnow()
        try:
            UserModel(**data)
        except TypeError:
            keys = ('name', 'last_name', 'email', 'cpf', 'genre', 'cellphone', 'birthdate', 'password')
            raise InvalidKeysError(f"Invalid Keys in body. Accepted Keys:{', '.join(keys)}")

        for key, value in data.items():
            setattr(self, key, value)

        self.save_self()