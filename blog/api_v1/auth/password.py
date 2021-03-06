from flask import g
from flask_restful import reqparse, Resource
from werkzeug.exceptions import Unauthorized

from blog.api_v1 import token_auth
from blog.api_v1.decorators import permission_required
from blog.models import Permission


parser = reqparse.RequestParser()
parser.add_argument(
    'old_password', location='json', required=True)
parser.add_argument(
    'new_password', location='json', required=True)


class Password(Resource):

    decorators = [permission_required(Permission.COMMENT),
                  token_auth.login_required]

    def post(self):
        args = parser.parse_args()
        verify = g.current_user.verify_password(args.old_password)
        if not verify:
            raise Unauthorized()
        g.current_user.update(password=args.new_password)
        return {}
