from flask import Blueprint
from app.controllers.adress_controller import (
    create_adress,
    read_adress,
    update_adress,
    delete_adress
)

bp = Blueprint('adresses_bp', __name__, url_prefix='/adress')

bp.post('')(create_adress)
bp.get('')(read_adress)
bp.patch('/<int:adress_id>')(update_adress)
bp.delete('/<int:adress_id>')(delete_adress)
