from flask import request, g

from app.api_v1 import BaseResource, token_auth
from app.models import Permission


class Token(BaseResource):

    @token_auth.login_required
    def get(self):
        code = self.UNAUTHORIZED_ACCESS
        print(code)
        if g.current_user.can(Permission.COMMENT):
            code = self.SUCCESS
        return {}, code
