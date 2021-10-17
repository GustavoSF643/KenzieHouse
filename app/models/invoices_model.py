from app.configs.database import db
from app.services.helper import DefaultModel
from sqlalchemy import Column, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship, backref
from dataclasses import dataclass
from datetime import datetime, timedelta

@dataclass
class InvoiceModel(db.Model, DefaultModel):
    invoice_id: int
    created_at: datetime
    due_date: datetime
    shipping_value: int
    products_value: int
    value: int
    __tablename__ = 'invoices'

    invoice_id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey('orders.order_id'))
    created_at = Column(DateTime, default=datetime.utcnow())
    due_date = Column(DateTime, default=datetime.utcnow() + timedelta(days=3))
    shipping_value = Column(Integer, nullable=False)
    products_value = Column(Integer, nullable=False)
    value = Column(Integer, nullable=False)

    order = relationship('OrderModel', backref=backref('invoice', uselist=False))
