import os

from flask import g
from flask_restful import Resource, reqparse
from werkzeug.datastructures import FileStorage

from blog import photos
from blog.models import Permission
from blog.api_v1 import token_auth
from blog.api_v1.decorators import permission_required


photo_reqparse = reqparse.RequestParser()
photo_reqparse.add_argument(
    'image',
    location='files',
    type=FileStorage,
    required=True
)


class PhotoStorage(Resource):

    method_decorators = [
        permission_required(Permission.ADMINISTER), token_auth.login_required
    ]

    def put(self):
        args = photo_reqparse.parse_args()
        if os.path.exists(
                os.path.join(photos.config.destination, str(g.current_user.id),
                             args.image.filename)):
            file_url = photos.url(
                os.path.join(str(g.current_user.id), args.image.filename))
        else:
            filename = photos.save(args.image, str(g.current_user.id))
            file_url = photos.url(filename)

        return {'url': file_url}
