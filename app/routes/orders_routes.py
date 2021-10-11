from flask import Blueprint
from app.controllers.order_controller import (
    create_order,
    read_order,
    update_order,
    delete_order
)

bp = Blueprint('orders_bp', __name__, url_prefix='/order')

bp.post('')(create_order)
bp.get('')(read_order)
bp.patch('/<int:order_id>')(update_order)
bp.delete('/<int:order_id>')(delete_order)
