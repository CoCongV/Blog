from flask import g
from flask_restful import Api, reqparse, abort, Resource
from flask_httpauth import HTTPBasicAuth

from ..models import User


auth = HTTPBasicAuth()


class Login(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('email', type=str, required=True, location='json')
        self.reqparse.add_argument('password', type=str, required=True, location='json')
        super(Login, self).__init__()

    @auth.verify_password
    def post(self):
        args = self.reqparse.parse_args()
        email = args['email']
        password = args['password']
        user = User.query.filter_by(email=email).first()
        verify = user.verify_password(password)
        if not verify:
            return False
        else:
            g.current_user = user
            return True
