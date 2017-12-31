import os

from flask import g, current_app
from flask_restful import Resource, reqparse
from werkzeug.datastructures import FileStorage

from app import photos
from app.api_v1 import token_auth
from app.api_v1.decorators import permission_required
from app.models import Permission, User
from app.utils.web import HTTPStatusCodeMixin

photo_reqparse = reqparse.RequestParser()
photo_reqparse.add_argument(
    'image', location='files', required=True, type=FileStorage)


class AvatarStroage(Resource, HTTPStatusCodeMixin):
    method_decorators = [
        permission_required(Permission.ADMINISTER),
        token_auth.login_required
    ]

    def put(self):
        args = photo_reqparse.parse_args()
        if os.path.exists(
                os.path.join(photos.config.destination, 'avatar',
                             args.get('image').filename)):
            file_url = photos.url(args.get('image').filename)
        else:
            filename = photos.save(args.get('image'), 'avatar')
            file_url = photos.url(filename)
            user = User.get(g.current_user.id)
            user.avatar = file_url
            user.save()
        return {'url': file_url}, self.CREATED
