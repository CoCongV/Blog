# from werkzeug.utils import secure_filename
from flask import request, g
from flask_restful import Resource

from app import photos
from app.models import Permission
from app.api_v1 import token_auth, HTTPStatusCodeMixin
from app.api_v1.decorators import permission_required
from app.api_v1.error import FileError
# from app.utils.tools import allowed_file


class PhotoStorage(Resource, HTTPStatusCodeMixin):
    @token_auth.login_required
    @permission_required(Permission.ADMINISTER)
    def post(self):
        if 'file' not in request.file:
            raise FileError("upload file not exist")

        filename = photos.save(request.files['photo'], g.current_user.id)
        file_url = photos.url(filename)
        return {'url': file_url}, self.CREATED
