from flask import request
from flask_restful import Resource

from app.api_v1 import HTTPStatusCode
from app.models import User


class UsernameExist(Resource, HTTPStatusCode):

    def get(self):
        username = request.args.get('username')
        user = User.query.filter_by(username=username)
        if user:
            return {}, self.USER_EXIST
        return {}, self.SUCCESS
