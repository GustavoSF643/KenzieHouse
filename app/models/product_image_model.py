from dataclasses import dataclass

from app.configs.database import db
from app.exceptions.product_exc import InvalidLinkError, ImageNotFoundError
from app.services.helper import DefaultModel
from environs import Env
from sqlalchemy import Column, Integer, String
from sqlalchemy.sql.schema import ForeignKey
from flask import send_from_directory
import os

env = Env()
env.read_env()


@dataclass
class ProductImageModel(db.Model, DefaultModel):

    name: str
    link: str
    type: str

    __tablename__ = 'product_image'

    product_image_id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey('products.product_id'))
    name = Column(String(127), nullable=False)
    link = Column(String(255), nullable=False, unique=True)
    type = Column(String(15), nullable=False)
    image_filename = Column(String(255), nullable=False)

    def download_image(self, image_name):
        image_type = '.' + self.type.split('/')[1]

        if self.image_filename != image_name:
            raise InvalidLinkError('Invalid link.')
        
        for _, _, filenames in os.walk(f"./{env('PRODUCT_IMAGE_FOLDER')}"):
            image_filename = image_name + image_type
            if image_filename not in filenames:
                raise ImageNotFoundError('Image not found.')

        
        product_image_folder = env('PRODUCT_IMAGE_FOLDER')
        file_path = self.image_filename + image_type
        filename = self.name

        return send_from_directory(
            directory=f"../{product_image_folder}", path=file_path, as_attachment=True, download_name=filename
        )


