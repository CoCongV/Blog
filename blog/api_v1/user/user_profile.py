from flask import g
from flask_restful import Resource, reqparse

from blog.models import User, Permission
from blog.api_v1 import token_auth


parser = reqparse.RequestParser()
parser.add_argument('uid', type=int, required=True)


class UserProfile(Resource):

    decorators = [token_auth.login_required]

    def get(self):
        # 权限分离
        args = parser.parse_args()
        user = User.get(args.uid)
        edit_permission = False
        if g.current_user == user or g.current_user.can(Permission.ADMINISTER):
            edit_permission = True

        return {
            "user": user.to_json(),
            "edit_permission": edit_permission
        }
