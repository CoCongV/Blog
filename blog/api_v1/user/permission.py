from flask import g
from flask_restful import reqparse, Resource

from blog.api_v1 import token_auth

permission_reqparse = reqparse.RequestParser()
permission_reqparse.add_argument(
    'permission', type=int, location='args', required=True)


class PermissionAuth(Resource):

    @token_auth.login_required
    def get(self):
        response = {'permission': 0}
        if not g.current_user.is_anonymous:
            response = {'permission': g.current_user.role.permissions}
        return response
