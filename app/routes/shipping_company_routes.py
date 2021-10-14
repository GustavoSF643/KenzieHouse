from app.controllers.shipping_company_controller import (
    create_shipping_company,
    get_shipping_company,
    get_shipping_company_by_id,
    update_shipping_company_by_id,
    delete_shipping_company_by_id
)
from flask import Blueprint

bp = Blueprint('shipping_company_bp', __name__, url_prefix='/shipping_company')

bp.post('')(create_shipping_company)
bp.get('')(get_shipping_company)
bp.get('/<int:id>')(get_shipping_company_by_id)
bp.patch('/<int:id>')(update_shipping_company_by_id)
bp.delete('/<int:id>')(delete_shipping_company_by_id)