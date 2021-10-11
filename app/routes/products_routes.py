from app.controllers.product_controller import (
    create_product,
    delete_product_by_id,
    get_product_by_id,
    get_products,
    update_product_by_id
)
from flask import Blueprint

bp = Blueprint('products_bp', __name__, url_prefix='/products')

bp.post('')(create_product)
bp.get('')(get_products)
bp.get('/<int:id>')(get_product_by_id)
bp.patch('/<int:id>')(update_product_by_id)
bp.delete('/<int:id>')(delete_product_by_id)
