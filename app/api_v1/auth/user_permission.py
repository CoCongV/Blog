from flask import g, request

from app.api_v1 import BaseResource, token_auth
from app.models import Permission, User


class UserPermission(BaseResource):

    decorators = [token_auth.login_required]

    def get(self):
        uid = request.args.get('uid')
        user = User.query.get(uid)
        if g.current_user == user and g.current_user.can(Permission.ADMINISTER):
            return {}, self.SUCCESS
        return {}, self.PERMISSION_FORBIDDEN
