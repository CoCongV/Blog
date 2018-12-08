import os
from pathlib import Path

from flask import g
from flask_restful import Resource, reqparse
from werkzeug.datastructures import FileStorage

from blog import photos
from blog.api_v1 import token_auth
from blog.api_v1.decorators import permission_required
from blog.models import Permission, User

photo_reqparse = reqparse.RequestParser()
photo_reqparse.add_argument(
    'image', location='files', required=True, type=FileStorage)


class AvatarStroage(Resource):
    method_decorators = [
        permission_required(Permission.COMMENT),
        token_auth.login_required
    ]

    def put(self):
        args = photo_reqparse.parse_args()
        file_format = args.image.filename.split('.')[-1]
        name = '%d-avatar.%s' % (g.current_user.id, file_format)
        path = Path(os.path.join(photos.config.destination, 'avatar', name))
        if path.exists():
            path.unlink()
        filename = photos.save(
            args.image,
            folder='avatar',
            name=name)
        file_url = photos.url(filename)
        g.current_user.avatar = file_url
        g.current_user.save()
        return {'url': file_url}
