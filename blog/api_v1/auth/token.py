from flask import g
from flask_restful import Resource

from blog.api_v1 import token_auth
from blog.utils.web import HTTPStatusCodeMixin
from blog.errors import AuthorizedError
from blog.models import Permission


class Token(Resource, HTTPStatusCodeMixin):

    @token_auth.login_required
    def get(self):
        if g.current_user.can(Permission.COMMENT):
            return {}, self.SUCCESS
        raise AuthorizedError()
