from flask import g
from flask_restful import Resource
from werkzeug.exceptions import Unauthorized

from blog.api_v1 import token_auth
from blog.models import Permission


class Token(Resource):

    @token_auth.login_required
    def get(self):
        if g.current_user.can(Permission.COMMENT):
            return {}
        raise Unauthorized()
