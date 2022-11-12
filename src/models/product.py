from dataclasses import dataclass
import datetime
from flask import jsonify, make_response
from sqlalchemy import DateTime
from .. import db
# from .security.simplehaszing import *
import os

RESPONSE_ERROR_FIELD_EXIST_CODE = os.getenv('RESPONSE_ERROR_FIELD_EXIST_CODE')
RESPONSE_ERROR_FIELD_TOO_SHORT = os.getenv('RESPONSE_ERROR_FIELD_TOO_SHORT')
RESPONSE_ERROR_WRONG_ARGUMENT = os.getenv('RESPONSE_ERROR_WRONG_ARGUMENT')
RESPONSE_ERROR_CANNOT_DELETE = os.getenv('RESPONSE_ERROR_CANNOT_DELETE')
RESPONSE_OK_DELETED = os.getenv('RESPONSE_OK_DELETED')
RESPONSE_OK_NOT_DELETED = os.getenv('RESPONSE_OK_NOT_DELETED')


@dataclass
class Product(db.Model):
    __tablename__ = "products"
    product_id = db.Column(db.Integer, primary_key=True)
    img = db.Column(db.String, nullable=False)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String, nullable=False)
    reg_date = db.Column(DateTime, default=datetime.datetime.utcnow)

    def to_json(self):
        return {
            'product_id': self.product_id,
            'img': self.img,
            'price': self.price,
            'quantity': self.quantity,
            'description': self.description,
            'reg_date': self.reg_date
        }

    def __init__(self, img: str, price: float, quantity: int, description: str):
        self.img = img
        self.price = price
        self.quantity = quantity
        self.description = description

    @staticmethod
    def __check_not_empty():
        # todo
        return True

    @staticmethod
    def create(img, price, quantity, description):

        # not_empty = Product.__check_not_empty()
        # if not_empty is not True:
        #     return make_response(not_empty, RESPONSE_ERROR_FIELD_EXIST_CODE)

        new_product = Product(img, price, quantity, description)

        db.session.add(new_product)
        db.session.commit()
        inserted_product = Product.get_by_id(new_product.product_id)
        return inserted_product

    @staticmethod
    def get_by_id(id):
        if type(id) is not int:
            return make_response("ID not numerical", RESPONSE_ERROR_WRONG_ARGUMENT)
        try:
            product = Product.query.get(id)
            db.session.commit()

        except:
            db.session.rollback()
        finally:
            if product is not None:
                return product.to_json()
            else:
                return make_response(
                    f"Product with id={id} does not exists", RESPONSE_ERROR_WRONG_ARGUMENT)

    @staticmethod
    def delete_by_id(id):
        if type(id) is not int:
            return make_response("ID not numerical", RESPONSE_ERROR_WRONG_ARGUMENT)

        try:
            deleted = Product.query.filter_by(product_id=id).delete()
            db.session.commit()
            if deleted == 1:
                return make_response("Succesfully deleted", RESPONSE_OK_DELETED)
            else:
                return make_response("Not deleted", RESPONSE_OK_NOT_DELETED)

        except:
            db.session.rollback()
            return make_response("Error", RESPONSE_OK_DELETED)

    @staticmethod
    def delete_all():
        num_rows_deleted = 0
        try:
            num_rows_deleted += db.session.query(Product).delete()
            db.session.commit()
        except:
            db.session.rollback()
        return jsonify(f'Deleted {num_rows_deleted} rows')

    @staticmethod
    def get_products():
        try:
            products = Product.query.all()
            db.session.commit()
        except:
            db.session.rollback()
        finally:
            return jsonify([product.to_json() for product in products])
