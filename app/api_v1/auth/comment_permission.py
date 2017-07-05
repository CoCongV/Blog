from flask import g
from flask_restful import Resource

from app.api_v1 import HTTPStatusCode, token_auth
from app.models import Permission


class CommentPermission(Resource, HTTPStatusCode):

    decorators = [token_auth.login_required]

    def get(self):
        if g.current_user.confirmed and g.current_user.can(Permission.COMMENT):
            return {}, self.SUCCESS
        return {'message': 'Email is not confirmed'}, self.PERMISSION_FORBIDDEN
