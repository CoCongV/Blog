from flask import g
from flask_restful import Resource, reqparse

from blog.models import User, Permission
from blog.api_v1 import token_auth
from blog.api_v1.decorators import permission_required


parser = reqparse.RequestParser()
parser.add_argument('uid', type=int, required=True)


class UserProfile(Resource):

    decorators = [
        permission_required(Permission.COMMENT), token_auth.login_required
    ]

    def get(self):
        args = parser.parse_args()
        user = User.get(args.uid)

        return {
            "user": user.to_json(),
        }
