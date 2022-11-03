#!/usr/bin/python
from crypt import methods
from datetime import datetime, timedelta
from functools import wraps
from flask import Flask, jsonify, make_response, render_template, request, session
import jwt
import os

import dbi

SECRET_KEY = os.getenv('SECRET_KEY')

DB_PATH = os.getenv('DB_PATH')

HOST = os.getenv('FLASK_HOST')
PORT = os.getenv('FLASK_PORT')

API_USER_LOGIN = os.getenv('API_USER_LOGIN')
API_USER_GET = os.getenv('API_USER_GET')
API_USER_CREATE = os.getenv('API_USER_CREATE')
API_USER_UPDATE = os.getenv('API_USER_UPDATE')
API_USER_DELETE = os.getenv('API_USER_DELETE')
API_USER_CHANGE_PASSWORD = os.getenv('API_USER_CHANGE_PASSWORD')


API_PRODUCT_GET = os.getenv('API_PRODUCT_GET')
API_PRODUCT_CREATE = os.getenv('API_PRODUCT_CREATE')
API_PRODUCT_UPDATE = os.getenv('API_PRODUCT_UPDATE')
API_PRODUCT_DELETE = os.getenv('API_PRODUCT_DELETE')


app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['SECRET_KEY'] = SECRET_KEY
db = dbi.Database(DB_PATH)
db.user_create()
db.product_create()


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.args.get('token')
        if not token:
            return jsonify({'message': 'Token is missing !!'}), 401

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
            print(f'decoded token:{data}')
        except:
            return jsonify({
                'message': 'Token is invalid !!'
            }), 401
        return f(*args, **kwargs)

    return decorated


@app.route('/')
def home():
    print(session.get('logged_in'))
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        return render_template('login.html')


@app.route('/welcome')
@token_required
def welcome():
    return render_template('welcome.html')


@app.route('/change-pass')
@token_required
def change_password_form():
    return render_template('change-pass.html')


@app.route('/search')
def search():
    return render_template('search.html')


@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')


@app.route('/product')
def product():
    return render_template('product.html')

#
# API
#

# @app.route('api/product/<product_id>', methods=['GET'])
# def handle_basket():
#     return jsonify(request.get_json())


@app.route(API_USER_LOGIN, methods=['POST'])
def handle_login():
    print("hello there")
    print(request.form)

    user = {
    }
    user['email'] = request.form['email']
    user['password'] = request.form['password']
    print(user)
    res = db.user_handle_login(user)
    print(f'res:{res}')
    if res:
        token = jwt.encode({
            'user': user['email'],
            'expiration': str(datetime.utcnow() + timedelta(seconds=60))
        },
            app.config['SECRET_KEY'])
        print('token:{token}')
        return jsonify({'token': token.decode('utf-8')})
    else:
        return make_response('Unable to verify', 408, {'WWW-Authenticate': 'Basic realm: "Authentication Failed "'})


@app.route(API_USER_CHANGE_PASSWORD, methods=['POST'])
@token_required
def change_password():
    token = request.args.get('token')
    email = request.form.get('email')
    password = request.form.get('password')
    password_2 = request.form.get('password_2')
    data = jwt.decode(token, app.config['SECRET_KEY'])
    print(data)
    token_email = data['user']
    print(
        f'token_email:{token_email}\nemail:{email}\npass:{password}\npass2:{password_2}')
    if (token_email != email) or (password != password_2):
        return make_response('Unable to change password', 444)

    db.users_change_password(email, password)
    return make_response(f'Password for:{email} changed', 222)


@app.route(API_USER_UPDATE+"/<user_id>", methods=['POST'])
def api_user_update_pass(user_id):
    return jsonify(db.users_update(request.get_json, user_id))


@app.route(API_USER_GET+"/<user_id>", methods=['GET'])
def api_user_get(user_id):
    return jsonify(db.user_get_by_id(user_id))


@app.route(API_USER_GET, methods=['GET'])
def api_users_get():
    return jsonify(db.users_get())


@app.route(API_USER_CREATE, methods=['POST'])
def api_user_create():
    return jsonify(db.user_insert(request.get_json()))


@app.route(API_PRODUCT_GET+"/<product_id>", methods=['GET'])
def api_product_get(product_id):
    return jsonify(db.product_get_by_id(product_id))


@app.route(API_PRODUCT_GET, methods=['GET'])
def api_products_get():
    return jsonify(db.products_get())


@app.route(API_PRODUCT_CREATE, methods=['POST'])
def api_product_create():
    print(request.get_json())
    return jsonify(db.product_insert(request.get_json()))


if __name__ == "__main__":
    app.run()
