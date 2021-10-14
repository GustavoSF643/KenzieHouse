from app.controllers.product_controller import (
    create_product,
    delete_product_by_id,
    get_product_by_id,
    get_products,
    get_image_product,
    update_product_by_id,
    upload_product_image_by_product_id
)
from flask import Blueprint

bp = Blueprint('products_bp', __name__, url_prefix='/products')

bp.post('')(create_product)
bp.post('/<int:product_id>')(upload_product_image_by_product_id)
bp.get('')(get_products)
bp.get('/<int:id>')(get_product_by_id)
bp.get('/<int:product_id>/<string:image_name>')(get_image_product)
bp.patch('/<int:id>')(update_product_by_id)
bp.delete('/<int:id>')(delete_product_by_id)
