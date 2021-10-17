from flask import Blueprint
from app.controllers.order_controller import (
    create_order,
    read_order,
    get_invoice_by_order_id,
    pay_invoice_by_order_id
)
from app.controllers.fiscal_note_controller import download_fiscal_note_by_order_id

bp = Blueprint('orders_bp', __name__, url_prefix='/order')

bp.post('')(create_order)
bp.get('')(read_order)
bp.get('/<int:order_id>/invoice')(get_invoice_by_order_id)
bp.post('/<int:order_id>/invoice')(pay_invoice_by_order_id)
bp.get('/<int:order_id>/fiscal_note')(download_fiscal_note_by_order_id)