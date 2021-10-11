from app.configs.database import db
from app.services.helper import DefaultModel
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from dataclasses import dataclass
from datetime import datetime

@dataclass
class OrderModel(db.Model, DefaultModel):
    status: str
    created_at: datetime
    __tablename__ = 'orders'

    order_id = Column(Integer, primary_key=True)
    status = Column(String, nullable=False, default='Aguardando Pagamento')
    created_at = Column(DateTime, default=datetime.utcnow())

    adress_id = Column(Integer, ForeignKey())
    # TODO -> Adiconar ForeignKey ao Criar tabela de orders_adresses
    shipping_company_id = Column(Integer, ForeignKey())
    # TODO -> Adicionar FOreignKey ao criar tabela de shipping_companies
    payment_method_id = Column(Integer, ForeignKey())
    # TODO -> Adiconar ForeignKey ao criar tabela de payment_methods