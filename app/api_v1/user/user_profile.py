from flask import g
from flask_restful import Resource, reqparse
from werkzeug.exceptions import Forbidden

from app.models import User, Permission
from app.api_v1 import token_auth
from app.utils.web import HTTPStatusCodeMixin


reqparse_patch = reqparse.RequestParser()
reqparse_patch.add_argument(
    'email', type=str, location='form', store_missing=True)
reqparse_patch.add_argument(
    'username', type=str, location='form', store_missing=True)
reqparse_patch.add_argument(
    'location', type=str, location='form', store_missing=True)
reqparse_patch.add_argument(
    'about_me', type=str, location='form', store_missing=True)
reqparse_patch.add_argument(
    'password', type=str, location='form', store_missing=True)


class UserProfile(Resource, HTTPStatusCodeMixin):

    decorators = [token_auth.login_required]

    def get(self, uid):
        # 权限分离
        user = User.query.get(uid)
        edit_permission = False
        if g.current_user == user or g.current_user.can(Permission.ADMINISTER):
            edit_permission = True

        return {
            "user": user.to_json(),
            "edit_permission": edit_permission
        }, self.SUCCESS

    def patch(self, uid):
        user = User.query.get(uid)
        if g.current_user != user:
            raise Forbidden()
        args = reqparse_patch.parse_args()
        g.current_user.update(**args)
        return {}, self.SUCCESS
