from flask import g
from flask_restful import Resource

from app.api_v1 import token_auth
from app.utils.web import HTTPStatusCodeMixin
from app.api_v1.error import AuthorizedError
from app.models import Permission


class Token(Resource, HTTPStatusCodeMixin):

    @token_auth.login_required
    def get(self):
        if g.current_user.can(Permission.COMMENT):
            return {}, self.SUCCESS
        raise AuthorizedError()
