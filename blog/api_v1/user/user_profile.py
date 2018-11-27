from flask import g
from flask_restful import Resource, reqparse

from blog.models import User, Permission
from blog.api_v1 import token_auth
from blog.api_v1.decorators import permission_required


parser = reqparse.RequestParser()
parser.add_argument('uid', type=int)


class UserProfile(Resource):

    decorators = [
        permission_required(Permission.COMMENT), token_auth.login_required
    ]

    def get(self):
        args = parser.parse_args()
        if args.uid:
            user = User.get(args.uid)
        else:
            user = g.current_user
        edit_permission = False
        if g.current_user == user or g.current_user.can(Permission.ADMINISTER):
            edit_permission = True

        return {
            "user": user.to_json(),
            "edit_permission": edit_permission
        }
