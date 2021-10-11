from flask import Blueprint
from app.controllers.user_controller import (
    create_user, 
    login_user, 
    read_user, 
    update_user, 
    delete_user,
    refresh_jwt_token
)

bp = Blueprint('users_bp', __name__)

bp.post('/register')(create_user)
bp.post('/login')(login_user)
bp.get('/user')(read_user)
bp.patch('/user')(update_user)
bp.delete('/user')(delete_user)
bp.post('/refresh')(refresh_jwt_token)