from flask import Blueprint
from app.controllers.adress_controller import (
    create_adress,
    read_adress,
    update_adress,
    delete_adress
)

bp = Blueprint('adresses_bp', __name__)

bp.post('/adress')(create_adress)
bp.get('/adress')(read_adress)
bp.put('/adress/<int:adress_id>')(update_adress)
bp.delete('/adress/<int:adress_id>')(delete_adress)
