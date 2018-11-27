from flask import g
from flask_restful import Resource

from blog.api_v1 import token_auth
from blog.models import comments


class UserComment(Resource):
    decorators = [
        token_auth.login_required
    ]

    def get(self):
        if g.current_user.is_anonymous:
            comments = list()
        else:
            comments = g.current_user.comments
        return {
            'comments': [i.to_json() for i in comments]
        }
