from dataclasses import dataclass
import datetime
from flask import jsonify, make_response
from sqlalchemy import DateTime
from .. import db
from sqlalchemy.sql import func
from .security.simplehaszing import *
import os

RESPONSE_ERROR_FIELD_EXIST_CODE = os.getenv('RESPONSE_ERROR_FIELD_EXIST_CODE')
RESPONSE_ERROR_FIELD_TOO_SHORT = os.getenv('RESPONSE_ERROR_FIELD_TOO_SHORT')
RESPONSE_ERROR_WRONG_ARGUMENT = os.getenv('RESPONSE_ERROR_WRONG_ARGUMENT')
RESPONSE_ERROR_CANNOT_DELETE = os.getenv('RESPONSE_ERROR_CANNOT_DELETE')
RESPONSE_OK_DELETED = os.getenv('RESPONSE_OK_DELETED')
RESPONSE_OK_NOT_DELETED = os.getenv('RESPONSE_OK_NOT_DELETED')


@dataclass
class User(db.Model):
    __tablename__ = "users"
    user_id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String, unique=True, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.BINARY(16), nullable=False)
    reg_date = db.Column(DateTime, default=datetime.datetime.utcnow)

    def to_json(self):
        return {
            'user_id': self.user_id,
            'nickname': self.nickname,
            'email': self.email,
            'password': self.password.decode('latin'),
            'reg_date': self.reg_date
        }

    def __init__(self, nickname: str, email: str, password: str):
        self.nickname = nickname
        self.email = email
        self.password = password

    @staticmethod
    def __check_unique(nickname, email):
        nickname_exists = db.session.query(User.user_id).filter_by(
            nickname=nickname).first() is not None
        email_exists = db.session.query(User.user_id).filter_by(
            email=email).first() is not None

        if nickname_exists:
            return f'Nickname: {nickname} already exists'

        if email_exists:
            return f'Email: {email} already exists'

        return True

    @staticmethod
    def __check_not_empty(nickname, email, password):
        CONST_NICKNAME_LEN = 1
        CONST_EMAIL_LEN = 1
        CONST_PASSWORD_LEN = 1

        if len(nickname) < CONST_NICKNAME_LEN:
            return f'Nickname len: {nickname} too small'

        if len(email) < CONST_EMAIL_LEN:
            return f'Email len: {email} too small'

        if len(password) < CONST_PASSWORD_LEN:
            return f'Password len: {password} too small'

        return True

    @staticmethod
    def create(nickname, email, password):

        unique = User.__check_unique(nickname, email)
        if unique is not True:
            return make_response(unique, RESPONSE_ERROR_FIELD_EXIST_CODE)

        not_empty = User.__check_not_empty(nickname, email, password)
        if not_empty is not True:
            return make_response(not_empty, RESPONSE_ERROR_FIELD_EXIST_CODE)

        SALT = str.encode(os.getenv('SALT'))
        password = hash_new_password(password, SALT)
        new_user = User(nickname, email, password)

        db.session.add(new_user)
        db.session.commit()
        inserted_user = User.get_by_id(new_user.user_id)
        return inserted_user

    @staticmethod
    def get_by_id(id):
        if type(id) is not int:
            return make_response("ID not numerical", RESPONSE_ERROR_WRONG_ARGUMENT)
        try:
            user = User.query.get(id)
            db.session.commit()

        except:
            db.session.rollback()
        finally:
            if user is not None:
                return jsonify(user.to_json())
            else:
                return make_response(
                    f"User with id={id} does not exists", RESPONSE_ERROR_WRONG_ARGUMENT)

    @staticmethod
    def delete_by_id(id):
        if type(id) is not int:
            return make_response("ID not numerical", RESPONSE_ERROR_WRONG_ARGUMENT)
        # deleted_user = User.query.filter_by(user_id=id).delete()
        # db.session.commit()
        # return jsonify(deleted_user)

        try:
            deleted = User.query.filter_by(user_id=id).delete()
            print(f'del:{deleted}')
            db.session.commit()
            if deleted == 1:
                return make_response("Succesfully deleted", RESPONSE_OK_DELETED)
            else:
                return make_response("Not deleted", RESPONSE_OK_NOT_DELETED)

        except:
            db.session.rollback()
            return make_response("Error", RESPONSE_OK_DELETED)

    @staticmethod
    def get_id_by_email(email):
        if not email:
            return make_response("Error", RESPONSE_ERROR_WRONG_ARGUMENT)

        try:
            user_by_email = User.query.filter_by(email=email).first()
            id = user_by_email.user_id
        except:
            db.session.rollback()
        return id

    @staticmethod
    def delete_all():
        num_rows_deleted = 0
        try:
            num_rows_deleted += db.session.query(User).delete()
            db.session.commit()
        except:
            db.session.rollback()
        return jsonify(f'Deleted {num_rows_deleted} rows')

    @staticmethod
    def get_users():
        # users = User.query.all()
        # return jsonify([user.to_json() for user in users])
        try:
            users = User.query.all()
            db.session.commit()
        except:
            db.session.rollback()
        finally:
            return jsonify([user.to_json() for user in users])

    @staticmethod
    def handle_login(email, password) -> bool:
        try:
            print("test")
            # user_by_email = User.query.filter_by(email=email)
            print(email)
            user_by_email = User.query.filter_by(email=email).first()
            # user_by_email.
            print("test")
            print(f'user_by_email:{user_by_email.password}')
            db.session.commit()
            if user_by_email is not None and user_by_email.password == password:
                print('true')
                return True
            else:
                return False

        except:
            db.session.rollback()
        # finally:
