import os

from flask import g
from flask_restful import Resource, reqparse
from werkzeug.datastructures import FileStorage

from app import photos
from app.models import Permission
from app.api_v1 import token_auth
from app.api_v1.decorators import permission_required
from app.utils.web import HTTPStatusCodeMixin


photo_reqparse = reqparse.RequestParser()
photo_reqparse.add_argument(
    'image',
    location='files',
    type=FileStorage,
    required=True
)


class PhotoStorage(Resource, HTTPStatusCodeMixin):

    method_decorators = [
        permission_required(Permission.ADMINISTER), token_auth.login_required
    ]

    def put(self):
        args = photo_reqparse.parse_args()
        if os.path.exists(
                os.path.join(photos.config.destination, str(g.current_user.id),
                             args.get('image').filename)):
            file_url = photos.url(
                os.path.join(
                    str(g.current_user.id),
                    args.get('image').filename))
        else:
            filename = photos.save(
                args.get('image'), str(g.current_user.id))
            file_url = photos.url(filename)

        return {'url': file_url}, self.CREATED
