from flask import redirect, url_for
from flask_restful import Resource

from app.api_v1 import HTTPStatusCode
from app.models import User


class EmailAuth(Resource, HTTPStatusCode):

    def get(self, token):
        result = User.verify_email_token(token)
        if result:
            return {}, self.SUCCESS
        return {}, self.UNAUTHORIZED_ACCESS
