from app.configs.database import db
from app.services.helper import DefaultModel
from sqlalchemy import Column, Integer, String
from dataclasses import dataclass

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