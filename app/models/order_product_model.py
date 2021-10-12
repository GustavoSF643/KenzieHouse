from sqlalchemy import Column, Integer, ForeignKey
from app.configs.database import db

orders_products = db.Table(
    'orders_product',
    Column('orders_product_id', Integer, primary_key=True),
    Column('order_id', Integer, ForeignKey('orders.order_id')),
    Column('product_id', Integer, ForeignKey('products.product_id')),
    Column('quantity', Integer),
    Column('total_value', Integer)
)