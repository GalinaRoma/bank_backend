from init import database


class CardPaymentDBModel(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    number = database.Column(database.String(16))
    date = database.Column(database.String(5))
    cvc = database.Column(database.String(3))
    payment = database.Column(database.Integer)
    comment = database.Column(database.String(150))
    email = database.Column(database.String)
    safety = database.Column(database.Boolean, default=True)


def add_to_card_db(message):
    message_to_db = CardPaymentDBModel(number=message['number'],
                                       date=message['date'],
                                       cvc=message['cvc'],
                                       payment=message['payment'],
                                       comment=message['comment'],
                                       email=message['email'])
    database.session.add(message_to_db)
    database.session.commit()


def change_safety(id):
    item = CardPaymentDBModel.query.filter_by(id=id).first()
    item.safety=not(item.safety)
    database.session.commit()


class RequestPaymentDBModel(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    sender = database.Column(database.String(12))
    bic = database.Column(database.String(9))
    destination = database.Column(database.String(20))
    payment = database.Column(database.Integer)
    vat = database.Column(database.String)
    email = database.Column(database.String)
    telephone = database.Column(database.String)


def add_to_request_db(message):
    message_to_db = RequestPaymentDBModel(sender=message['sender'],
                                        bic=message['bic'],
                                        destination=message['destination'],
                                        payment=message['payment'],
                                        vat=message['vat'],
                                        email=message['email'],
                                        telephone = message['telephone'])
    database.session.add(message_to_db)
    database.session.commit()


class AuthDBModel(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    login = database.Column(database.String)
    hash_password = database.Column(database.String)
    salt = database.Column(database.String)


def get_password_hashDB(username):
    user = AuthDBModel.query.filter_by(username=username).first()
    return user.password_hash


def get_salt(username):
    user = AuthDBModel.query.filter_by(username=username).first()
    return user.salt
