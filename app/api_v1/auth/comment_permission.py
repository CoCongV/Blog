from flask import g
from flask_restful import Resource

from app.api_v1 import token_auth
from app.api_v1.error import PermissionForbiddenError
from app.models import Permission
from app.utils.web import HTTPStatusCodeMixin


class CommentPermission(Resource, HTTPStatusCodeMixin):

    decorators = [token_auth.login_required]

    def get(self):
        if g.current_user.confirmed and g.current_user.can(Permission.COMMENT):
            return {}, self.SUCCESS
        return PermissionForbiddenError()
