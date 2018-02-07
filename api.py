import secrets

from flask import request, send_file
from flask_restful import Resource
from database import CardPaymentDBModel, add_to_card_db, change_safety, RequestPaymentDBModel, add_to_request_db, \
    AuthDBModel
from authorization import get_password, hash_password, encode_auth_token, decode_auth_token


def general_get(model):
    models = model.query.all()
    for e in models:
        e.__dict__.pop('_sa_instance_state')
    try:
        return list(map(lambda x: x.__dict__, models))
    except Exception:
        return {}, 400

tokens = []
class SecurityAPI(Resource):
    def get(self):
        cur_token = secrets.token_hex(10)
        tokens.append(cur_token)
        return {'token': cur_token}, 200


class CardPaymentAPI(Resource):
    def get(self):
        return general_get(CardPaymentDBModel)

    def post(self):
        message = request.get_json()
        if message is not None and self.is_valid(message):
            if message['token'] in tokens:
                add_to_card_db(message)
                return {"ok": "true"}, 200
            else:
                return {}, 403
        return {}, 400

    def put(self, id):
        try:
            change_safety(id)
            return {"ok": "true"}, 200
        except Exception as e:
            print(e)
            return {}, 404

    def is_valid(self, message):
        return True


class RequestPaymentAPI(Resource):
    def get(self):
        return general_get(RequestPaymentDBModel)

    def post(self):
        message = request.get_json()
        if message is not None and self.is_valid(message):
            add_to_request_db(message)
            return {"ok": "true"}, 200
        return {}, 400

    def is_valid(self, message):
        return True


class BankPaymentAPI(Resource):
    def post(self):
        message = request.get_json()
        if message is not None and self.is_valid(message):
            return self.transform_to_file(message)
        return {}, 400

    def transform_to_file(self, message):
        with open("bank.txt", 'w', encoding='utf-8') as file:
            file.write(str(message))
            return send_file("bank.txt")

    def is_valid(self, message):
        return True


class LoginApi(Resource):
    def post(self):
        data = request.get_json()
        try:
            user = AuthDBModel.query.filter_by(username=data['username']).first()
            if user and get_password(data['username']) == hash_password(data['username'], data['password']):
                token = encode_auth_token(user.id)
                if token:
                    return {
                        'ok': 'true',
                        'message': 'Logged in',
                        'auth_token': token.decode()
                    }
            else:
                return {
                           'ok': 'false',
                           'message': 'Invalid credentials'
                       }, 403
        except Exception as e:
            print(e)
            return {
                       'ok': 'false',
                       'message': 'Internal error, try again later'
                   }, 500

    def get(self):
        auth_header = request.headers.get('Authorization')
        if auth_header:
            token = auth_header.split()[1]
        else:
            token = ''
        if token:
            resp = decode_auth_token(token)
            if not isinstance(resp, str):
                user = Admin.query.filter_by(id=resp).first()
                response_obj = {
                    'ok': 'true',
                    'data': {
                        'user_id': user.id,
                        'username': user.username
                    }
                }
                return response_obj
            return {
                       'ok': 'false',
                       'message': resp
                   }, 403
        else:
            return {
                       'ok': 'false',
                       'message': 'Invalid token.'
                   }, 403