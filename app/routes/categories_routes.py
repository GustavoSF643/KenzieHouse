from app.controllers.category_controller import (
    create_category,
    delete_category_by_id,
    get_categories,
    get_category_by_id,
    get_products_by_category_id,
    update_category_by_id
)
from flask import Blueprint

bp = Blueprint('categories_bp', __name__, url_prefix='/categories')

bp.post('')(create_category)
bp.get('')(get_categories)
bp.get('/<int:id>')(get_category_by_id)
bp.get('<int:category_id>/products')(get_products_by_category_id)
bp.patch('/<int:id>')(update_category_by_id)
bp.delete('/<int:id>')(delete_category_by_id)
