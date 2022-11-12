from flask import Blueprint, jsonify, redirect, render_template, request, url_for
from src.models.user import User
from ..models.security.jwt import handle_login, token_required, logout
import os

API_USER_LOGIN = os.getenv('API_USER_LOGIN')
API_USER_GET = os.getenv('API_USER_GET')
API_USER_CREATE = os.getenv('API_USER_CREATE')
API_USER_UPDATE = os.getenv('API_USER_UPDATE')
API_USER_DELETE = os.getenv('API_USER_DELETE')
API_USER_CHANGE_PASSWORD = os.getenv('API_USER_CHANGE_PASSWORD')

bp = Blueprint('user', __name__)

# todo: change pass template + user info on nav


@bp.route(API_USER_GET, methods=["GET"])
def api_user_get():
    users = User.get_users()
    return users


@bp.route(API_USER_GET+"/<int:id>", methods=["GET"])
def api_user_get_by_id(id=None):
    if id is not None:
        users = User.get_by_id(id)
        return users


@bp.route(API_USER_CREATE, methods=["POST", "GET"])
def api_user_create():
    if request.method == "GET":
        return render_template("sign-up.html")
    nickname = request.form['nickname']
    email = request.form['email']
    password = request.form['password']
    user = User.create(nickname, email, password)
    return user


@bp.route(API_USER_LOGIN, methods=["POST", "GET"])
def api_user_login():
    if request.method == "GET":
        return render_template("login.html")
    # nickname = request.form['nickname']
    email = request.form['email']
    password = request.form['password']
    return handle_login(email, password)
    # return user


@bp.route(API_USER_DELETE, methods=["DELETE"])
@token_required
def api_user_delete():
    return User.delete_all()


@bp.route(API_USER_DELETE+"/<int:id>", methods=["DELETE"])
@token_required
def api_user_delete_by_id(id=None):
    if id is not None:
        return User.delete_by_id(id)


@bp.route("/")
@token_required
def root():
    return redirect(url_for('product.product'))


@bp.route("/logout")
@token_required
def user_logout():
    logout()
    return render_template('login.html')
