from functools import wraps

from flask import jsonify, redirect, session, url_for


from datetime import datetime, timedelta
from functools import wraps
from flask import jsonify, make_response, render_template, session
import jwt
import os

from src.models.security.simplehaszing import hash_new_password
from src.models.user import User

SECRET_KEY = os.getenv('SECRET_KEY')
TOKEN_EXPIRATION_IN_SECONDS = int(os.getenv('TOKEN_EXPIRATION_IN_SECONDS'))
SESSION_USER_EMAIL = os.getenv('SESSION_USER_EMAIL')
SESSION_USER_TOKEN = os.getenv('SESSION_USER_TOKEN')
SALT = str.encode(os.getenv('SALT'))


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        # token = request.args.get('token')
        if SESSION_USER_TOKEN not in session:
            # if not token:
            return render_template('login.html')
            return jsonify({'message': 'Token is missing !!'}), 401

        try:
            data = __decode_token(session[SESSION_USER_TOKEN])

            if __check_token_expired(data):
                logout()
                return render_template('login.html')

            if data['email'] != session[SESSION_USER_EMAIL]:
                return jsonify({'message': 'Token not match to user !!'}), 401
            print(f'decoded token:{data}')
        except:
            return jsonify({
                'message': 'Token is invalid !!'
            }), 401
        return f(*args, **kwargs)

    return decorated


def __encode_token(email):
    token = jwt.encode({
        'email': email,
        'expiration': str(datetime.utcnow() + timedelta(seconds=TOKEN_EXPIRATION_IN_SECONDS))
    },
        SECRET_KEY, algorithm="HS256")
    return token


def __decode_token(encoded):
    token = jwt.decode(encoded, SECRET_KEY, algorithms="HS256")
    return token


def __check_token_expired(token):
    token_expiration = token['expiration']
    try:
        format = "%Y-%m-%d %H:%M:%S.%f"
        past = datetime.strptime(token_expiration, format)
    except:
        return make_response("Faile to check token expiration date", 555)
    present = datetime.utcnow()
    return past < present


def logout():
    session.pop(SESSION_USER_TOKEN, None)


def handle_login(email, password):
    if SESSION_USER_TOKEN in session:
        return render_template('welcome.html')

    hashed_password = hash_new_password(password, SALT)
    res = User.handle_login(email, hashed_password)

    if res:
        token = __encode_token(email)
        session[SESSION_USER_TOKEN] = token
        session[SESSION_USER_EMAIL] = email
        print(f'encoded:{token}')
        return redirect(url_for('product.product'))
    else:
        return make_response('Unable to verify', 408, {'WWW-Authenticate': 'Basic realm: "Authentication Failed "'})


def is_admin():
    email = session[SESSION_USER_EMAIL]
    user = User.get_by_id(User.get_id_by_email(email))
    is_admin = user.get_json()['is_admin']
    print(f"is_admin:{is_admin}")
    if is_admin:
        return True
    else:
        return False
