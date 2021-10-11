from app.configs.database import db
from app.services.helper import DefaultModel
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import backref, relationship
from werkzeug.security import generate_password_hash, check_password_hash
from dataclasses import dataclass
from datetime import datetime

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

    @property
    def password(self):
        raise AttributeError("Password cannot be accessed!")

    @password.setter
    def password(self, password_to_hash):
        self.password_hash = generate_password_hash(password_to_hash)

    def validate_password(self, password_to_validate):
        return check_password_hash(self.password_hash, password_to_validate)

    def update(self):
        self.updated_at = datetime.utcnow()