from api import CardPaymentAPI, RequestPaymentAPI, BankPaymentAPI, SecurityAPI
from init import app, api
from database import *

api.add_resource(CardPaymentAPI, '/cardPayment/<int:id>', endpoint='cardPaymentId')
api.add_resource(CardPaymentAPI, '/cardPayment', endpoint='cardPayment')
api.add_resource(RequestPaymentAPI, '/requestPayment', endpoint='requestPayment')
api.add_resource(BankPaymentAPI, '/bankPayment', endpoint='bankPayment')
api.add_resource(SecurityAPI, '/security', endpoint='security')
database.create_all()

if __name__ == '__main__':
    app.run(port = 2700, debug = True)