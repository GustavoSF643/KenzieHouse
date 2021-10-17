from app.configs.database import db
from app.services.helper import DefaultModel
from sqlalchemy import Column, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship, backref
from datetime import datetime, timedelta
from app.exceptions.invoice_exc import ExpiredInvoiceError

class InvoiceModel(db.Model, DefaultModel):
    __tablename__ = 'invoices'

    invoice_id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey('orders.order_id'))
    created_at = Column(DateTime, default=datetime.utcnow())
    due_date = Column(DateTime, default=datetime.utcnow() + timedelta(days=3))
    shipping_value = Column(Integer, nullable=False)
    products_value = Column(Integer, nullable=False)
    value = Column(Integer, nullable=False)

    order = relationship('OrderModel', backref=backref('invoice', uselist=False))

    def format_self(self):
        return {
            'invoice_id': self.invoice_id,
            'created_at': datetime.strftime(self.created_at, '%d/%m/%Y %H:%M:%S %p'),
            'due_date': datetime.strftime(self.due_date, '%d/%m/%Y %H:%M:%S %p'),
            'shipping_value': self.shipping_value,
            'products_value': self.products_value,
            'value': self.value
        }

    def verify_invoice_due_date(self):
        today = datetime.utcnow()

        if today > self.due_date:
            raise ExpiredInvoiceError('Cannot pay a invoice with expired due date.')
