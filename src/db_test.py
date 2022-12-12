import os
from unittest import TestCase

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
# from ..ssrc
# from src import *
from .models.user import User
from .models.order import Order
from .models.product import Product

import pytest
from . import init_test_app, db


# from flask.ext.testing import TestCase

# from myapp import create_app, db
class MyTest():

    # I removed some config passing here
    def create_app(self):
        return init_test_app()

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()


test = MyTest()
test.create_app()
test.setUp()

Order.delete_all()
User.delete_all()
Product.delete_all()


def test_delete_users():

    # arrange

    # act

    User.delete_all()
    users_after = User.get_users()

    # assert
    assert len(users_after.json) == 0


def test_create_user_admin():

    # arrange
    users_before = User.get_users()
    # act
    u = User.create("vsgsgsbo", "smsegfeiogef", "amsegosfie", True)
    users_after = User.get_users()

    # assert
    assert len(users_before.json) + 1 == len(users_after.json)
    assert u.get_json()['is_admin'] == True
    # clean
    User.delete_all()


def test_create_user_basic():

    # arrange
    users_before = User.get_users()
    # act
    u = User.create("adminvsgsgsbo", "adminsmsegfeiogef",
                    "aaaamsegosfie", False)
    users_after = User.get_users()

    # assert
    assert len(users_before.json) + 1 == len(users_after.json)
    assert u.get_json()['is_admin'] == False
    # clean
    User.delete_all()


def test_not_allow_to_create_user_with_same_email():
    # arrange
    users_before = User.get_users()
    # act
    u = User.create("1adminvsgsgsbo", "adminsmsegfeiogef",
                    "aaaamsegosfie", False)
    u2 = User.create("2adminvsgsgsbo", "adminsmsegfeiogef",
                     "aaaamsegosfie", False)
    users_after = User.get_users()

    # assert
    assert len(users_before.json) + 1 == len(users_after.json)
    assert u.get_json()['is_admin'] == False
    # clean
    User.delete_all()


def test_not_allow_to_create_user_with_same_nickname():
    # arrange
    users_before = User.get_users()
    # act
    u = User.create("same", "nofasofgba",
                    "aaaamsegosfie", False)
    u2 = User.create("same", "123",
                     "aaaamsegosfie", False)
    users_after = User.get_users()

    # assert
    assert len(users_before.json) + 1 == len(users_after.json)
    assert u.get_json()['is_admin'] == False
    # clean
    User.delete_all()


def test_make_wrong_order():
    # arrange
    # act
    quanti = 14
    p = Product.create("img", 12, quanti, "aaaa", 12)
    new_p = Product.get_by_id(p['product_id'])
    u = User.create("random", "aswkfnqwiouf", "fwniogweifwbgoiweg", False)
    # new_u = User.get_by_id(u["user_id"])
    print(u.get_json()['user_id'])
    try:
        o = Order.create(u.get_json()['user_id'],
                         [new_p['product_id']], [quanti+1], True)
    except:
        assert True
    Order.delete_all()
    User.delete_all()
    Product.delete_all()


def test_make_good_order():
    # arrange
    # act
    quanti = 14
    p = Product.create("img", 12.0, quanti, "aaaa", 12)
    new_p = Product.get_by_id(p['product_id'])
    u = User.create("random", "aswkfnqwiouf", "fwniogweifwbgoiweg", False)
    # new_u = User.get_by_id(u["user_id"])
    print(u.get_json()['user_id'])
    try:
        o = Order.create(u.get_json()['user_id'],
                         [new_p['product_id']], [quanti+1], True)
    except:
        assert False
    Order.delete_all()
    User.delete_all()
    Product.delete_all()
