from app.controllers.category_controller import (
    create_category,
    delete_category_by_id,
    get_categories,
    get_category_by_id,
    update_category_by_id
)
from flask import Blueprint

bp = Blueprint('categories', __name__, url_prefix='/categories')

bp.post('')(create_category)
bp.get('')(get_categories)
bp.get('/<int:id>')(get_category_by_id)
bp.patch('/<int:id>')(update_category_by_id)
bp.delete('/<int:id>')(delete_category_by_id)
