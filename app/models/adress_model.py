from sqlalchemy.orm import relationship
from app.configs.database import db
from app.services.helper import DefaultModel
from sqlalchemy import Column, Integer, String, ForeignKey
from dataclasses import dataclass

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