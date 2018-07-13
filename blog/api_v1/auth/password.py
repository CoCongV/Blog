from flask import g
from flask_restful import reqparse, Resource
from werkzeug.exceptions import Unauthorized

from blog.api_v1 import token_auth
from blog.api_v1.decorators import permission_required
from blog.models import Permission


reparse = reqparse.RequestParser()
reqparse.add_argument(
    'old_password', location='json', required=True)
reqparse.add_argument(
    'new_password', location='json', required=True)


class Password(Resource):

    decorators = [permission_required(Permission.COMMENT),
                  token_auth.login_required]

    def post(self):
        args = reqparse.parse_args()
        old_password = args['old_password']
        new_password = args['new_password']
        verify = g.current_user.verify_password(old_password)
        if not verify:
            raise Unauthorized()
        g.current_user.update(password=new_password)
        return {}
