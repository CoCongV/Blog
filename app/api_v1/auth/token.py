from flask import g
from flask_restful import Resource

from app.api_v1 import HTTPStatusCode, token_auth
from app.models import Permission


class Token(Resource, HTTPStatusCode):

    @token_auth.login_required
    def get(self):
        code = self.UNAUTHORIZED_ACCESS
        print(code)
        if g.current_user.can(Permission.COMMENT):
            code = self.SUCCESS
        return {}, code
