from dataclasses import dataclass
import datetime
from flask import jsonify, make_response
from sqlalchemy import DateTime
from sqlalchemy.sql import expression
from src.models.user import User
from .. import db
from .product import Product
import os

RESPONSE_ERROR_FIELD_EXIST_CODE = os.getenv('RESPONSE_ERROR_FIELD_EXIST_CODE')
RESPONSE_ERROR_FIELD_TOO_SHORT = os.getenv('RESPONSE_ERROR_FIELD_TOO_SHORT')
RESPONSE_ERROR_WRONG_ARGUMENT = os.getenv('RESPONSE_ERROR_WRONG_ARGUMENT')
RESPONSE_ERROR_CANNOT_DELETE = os.getenv('RESPONSE_ERROR_CANNOT_DELETE')
RESPONSE_OK_DELETED = os.getenv('RESPONSE_OK_DELETED')
RESPONSE_OK_NOT_DELETED = os.getenv('RESPONSE_OK_NOT_DELETED')
RESPONSE_DOES_NOT_EXIST = os.getenv('RESPONSE_DOES_NOT_EXIST')


order_product = db.Table('order_product',
                         db.Column('product_id', db.Integer,
                                   db.ForeignKey('products.product_id')),
                         db.Column('order_id', db.Integer,
                                   db.ForeignKey('orders.order_id'))
                         )
#  ,db.Column('quantity', db.Integer)


@dataclass
class Order(db.Model):
    __tablename__ = "orders"
    order_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(
        "users.user_id"), nullable=False)
    products = db.relationship(
        'Product', secondary=order_product, backref='orders')
    reg_date = db.Column(DateTime, default=datetime.datetime.utcnow)
    bought = db.Column(
        db.Boolean, server_default=expression.true(), nullable=False)

    def to_json(self):
        return {
            'order_id': self.order_id,
            'user_id': self.user_id,
            # 'products': ''.join([product for product in self.products]),
            'reg_date': self.reg_date
        }

    def __init__(self, user_id: int, bought=True):
        self.user_id = user_id
        self.bought = bought

    @staticmethod
    def __check_not_empty():
        # todo
        return True

    @staticmethod
    def create(user_id, products_ids, bought):

        if db.session.query(User).get(user_id) is None:
            return make_response(f'User with id={user_id} does not exists', RESPONSE_DOES_NOT_EXIST)

        new_order = Order(user_id, bought)
        # todo: add quantity to order, dec quantity after makeOrder (+validate) + ?bought?

        for p in products_ids:
            product = db.session.query(Product).get(p)
            new_order.products.append(product)
            db.session.add(product)

        db.session.add(new_order)
        db.session.commit()
        inserted_order = Order.get_by_id(new_order.order_id)
        return inserted_order

    @staticmethod
    def get_by_id(id):
        if type(id) is not int:
            return make_response("ID not numerical", RESPONSE_ERROR_WRONG_ARGUMENT)
        try:
            order = Order.query.get(id)
            db.session.commit()

        except:
            db.session.rollback()
        finally:
            if order is not None:
                return jsonify(order.to_json())
            else:
                return make_response(
                    f"Order with id={id} does not exists", RESPONSE_ERROR_WRONG_ARGUMENT)

    @staticmethod
    def get_by_bought(bought):
        orders = []
        try:
            orders = User.query.filter_by(bought=bought)
            db.session.commit()
        except:
            db.session.rollback()
        finally:
            return orders

    @staticmethod
    def get_by_user_id(user_id):
        orders_classified = {}
        try:
            orders = Order.query.filter_by(user_id=user_id)
            orders_classified = {}

            for o in orders:
                ps = []
                for p in o.products:
                    ps.append(p.to_json())
                orders_classified[(o.order_id, o.reg_date)] = ps

            db.session.commit()
        except:
            db.session.rollback()
        finally:
            return orders_classified
    # @staticmethod
    # def delete_by_id(id):
    #     if type(id) is not int:
    #         return make_response("ID not numerical", RESPONSE_ERROR_WRONG_ARGUMENT)

    #     try:
    #         deleted = Product.query.filter_by(product_id=id).delete()
    #         db.session.commit()
    #         if deleted == 1:
    #             return make_response("Succesfully deleted", RESPONSE_OK_DELETED)
    #         else:
    #             return make_response("Not deleted", RESPONSE_OK_NOT_DELETED)

    #     except:
    #         db.session.rollback()
    #         return make_response("Error", RESPONSE_OK_DELETED)

    @staticmethod
    def delete_all():
        num_rows_deleted = 0
        num_rows_deleted_relation = 0
        try:
            num_rows_deleted += db.session.query(Order).delete()
            num_rows_deleted_relation += db.session.query(
                order_product).delete()
            db.session.commit()
        except:
            db.session.rollback()
        return jsonify(f'Deleted {num_rows_deleted} rows from Order && Deleted {num_rows_deleted_relation} rows from Order_Product realation  ')

    # @staticmethod
    # def get_products():
    #     try:
    #         products = Product.query.all()
    #         db.session.commit()
    #     except:
    #         db.session.rollback()
    #     finally:
    #         return jsonify([product.to_json() for product in products])

    # @staticmethod
    # def drop():

    #     # order_product.drop(engine)
    #     # Order.__table__.drop(engine)

    #     engine = sqlalchemy.create_engine('sqlite:///instance/shop.db')
    #     Order.__table__.drop()
    #     order_product.__table__.drop()
