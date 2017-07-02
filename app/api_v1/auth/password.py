from flask import g
from flask_restful import reqparse

from app.api_v1 import BaseResource, token_auth, permission_required
from app.models import Permission
from app.lib.send_mail import send_email


class Password(BaseResource):

    decorators = [permission_required(Permission.COMMENT),
                  token_auth.login_required]

    def __init__(self):
        super(Password, self).__init__()
        self._reqparse = reqparse.RequestParser()

    def post(self):
        self._reqparse.add_argument('old_password', location='json', required=True)
        self._reqparse.add_argument('new_password', location='json', required=True)
        args = self._reqparse.parse_args()
        old_password = args['old_password']
        new_password = args['new_password']
        verify = g.current_user.verify_passwor(old_password)
        if not verify:
            return {}, self.UNAUTHORIZED_ACCESS
        g.current_user.update(password=new_password)
        return {}, self.SUCCESS
