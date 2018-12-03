from flask import g
from flask_restful import Resource, reqparse

from blog.models import User, Permission
from blog.api_v1 import token_auth
from blog.api_v1.decorators import permission_required


class UserProfile(Resource):

    def get(self, uid):
        user = User.get(uid).to_json()
        return {
            'avatar': user['avatar'],
            'email': user['email'],
            'username': user['username'],
            'about_me': user['about_me'],
            'member_since': user['member_since'],
        }
