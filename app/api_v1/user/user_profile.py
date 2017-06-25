from flask import g

from app.models import User, Permission
from app.api_v1 import BaseResource, token_auth


class UserProfile(BaseResource):

    decorators = [token_auth.login_required]

    def get(self, uid):
        user = User.query.get(uid)
        edit_permission = False
        if g.current_user == user or g.current_user.can(Permission.ADMINISTER):
            edit_permission = True

        return {
            "user": user.to_json(),
            "edit_permission": edit_permission
        }, 200
