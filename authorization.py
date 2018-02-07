import hashlib, jwt, datetime
from database import get_salt, get_password_hashDB
from init import app


def encode_auth_token(user_id):
    try:
        payload = {
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1),
            'iat': datetime.datetime.utcnow(),
            'sub': user_id
        }
        return jwt.encode(payload, app.config['SECRET_KEY'], algorithm='HS256')
    except Exception as e:
        print(e)
        return e


def decode_auth_token(token):
    try:
        payload = jwt.decode(token, app.config['SECRET_KEY'])
        return payload['sub']
    except jwt.ExpiredSignatureError:
        return 'Signature expired. Please log in again.'
    except jwt.InvalidTokenError:
        return 'Invalid token. Please log in again.'


def hash_password(username, password):
    salt = get_salt(username)
    cur_hash = hashlib.sha256()
    cur_hash.update(salt.encode())
    cur_hash.update(password.encode())
    return cur_hash.hexdigest()


def get_password(username):
    return get_password_hashDB(username)