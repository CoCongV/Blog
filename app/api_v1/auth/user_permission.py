from flask import g, request
from flask_restful import Resource

from app.api_v1 import HTTPStatusCodeMixin, token_auth
from app.api_v1.error import PermissionForbiddenError
from app.models import Permission, User


class UserPermission(Resource, HTTPStatusCodeMixin):

    decorators = [token_auth.login_required]

    def get(self):
        uid = request.args.get('uid')
        user = User.query.get(uid)
        if g.current_user == user and g.current_user.can(Permission.ADMINISTER):
            return {}, self.SUCCESS
        raise PermissionForbiddenError()
