from flask import g
from flask_restful import reqparse, Resource

from ..models import User
from . import api, auth


class GetUserInfo(Resource):

    @auth.login_required
    def get(self):
        user = g.current_user.json()
        return user, 200


api.add_resource(GetUserInfo, '/user/')
