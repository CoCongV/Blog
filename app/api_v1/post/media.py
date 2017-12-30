from flask import request, g
from flask_restful import Resource

from app import photos
from app.errors import FileError
from app.models import Permission
from app.api_v1 import token_auth
from app.api_v1.decorators import permission_required
from app.utils.web import HTTPStatusCodeMixin


class PhotoStorage(Resource, HTTPStatusCodeMixin):

    @token_auth.login_required
    @permission_required(Permission.ADMINISTER)
    def post(self):
        print(request.files)
        if 'image' not in request.files:
            raise FileError("upload file not exist")

        filename = photos.save(request.files['image'], str(g.current_user.id))
        print(filename)
        print(photos.path(filename))
        file_url = photos.url(filename)
        return {'url': file_url}, self.CREATED
