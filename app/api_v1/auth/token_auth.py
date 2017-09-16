from flask_restful import Resource

from app.utils.web import HTTPStatusCodeMixin
from app.api_v1.error import AuthorizedError
from app.models import User


class EmailAuth(Resource, HTTPStatusCodeMixin):

    def get(self, token):
        result = User.verify_email_token(token)
        if result:
            return {}, self.SUCCESS
        return AuthorizedError()
