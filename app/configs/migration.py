from flask import Flask
from flask_migrate import Migrate

def init_app(app: Flask):
    # Aqui vem os import de models
    from app.models.user_model import UserModel
    from app.models.adress_model import AdressModel
    from app.models.category_model import CategoryModel
    from app.models.product_model import ProductModel
    
    Migrate(app, app.db, compare_type=True)
