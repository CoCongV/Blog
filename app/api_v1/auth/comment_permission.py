from flask import g, request

from app.api_v1 import BaseResource, token_auth
from app.models import Permission, User


class CommentPermission(BaseResource):

    decorators = [token_auth.login_required]

    def get(self):
        if g.current_user.confirmed and g.current_user.can(Permission.COMMENT):
            return {}, self.SUCCESS
        return {'message': 'Email is not confirmed'}, self.PERMISSION_FORBIDDEN
