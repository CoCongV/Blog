from flask import redirect, url_for

from app.api_v1 import BaseResource
from app.models import User


class EmailAuth(BaseResource):

    def get(self, token):
        result = User.verify_email_token(token)
        if result:
            return {}, self.SUCCESS
        return {}, self.UNAUTHORIZED_ACCESS
