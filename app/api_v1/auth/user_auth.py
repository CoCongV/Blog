from flask import request
from flask_restful import Resource

from app.api_v1 import HTTPStatusCodeMixin
from app.models import User
from app.api_v1.error import UserAlreadyExistsError


class UsernameExist(Resource, HTTPStatusCodeMixin):

    def get(self):
        username = request.args.get('username')
        user = User.query.filter_by(username=username).first()
        if user:
            raise UserAlreadyExistsError()
        return {}, self.SUCCESS
