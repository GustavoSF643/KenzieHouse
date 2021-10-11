from flask import Blueprint
from app.controllers.payment_controller import (
    create_payment,
    get_payments,
    get_payment_by_id,
    update_payment_by_id,
    delete_payment_by_id
)

bp = Blueprint('payment_bp', __name__, url_prefix='/payment')

bp.post('')(create_payment)
bp.get('')(get_payments)
bp.get('<int:id>')(get_payment_by_id)
bp.patch('<int:id>')(update_payment_by_id)
bp.delete('<int:id>')(delete_payment_by_id)
