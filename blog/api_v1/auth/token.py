from flask import g
from flask_restful import Resource
from werkzeug.exceptions import BadRequest

from blog.api_v1 import token_auth
from blog.models import Permission


class Token(Resource):

    @token_auth.login_required
    def get(self):
        if g.current_user.can(Permission.COMMENT):
            return {
                'state': True,
                'username': g.current_user.username,
                'permission': g.current_user.role.permissions,
                'avatar': g.current_user.avatar
            }
        return {'state': False}
