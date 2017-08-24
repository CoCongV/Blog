import os

from werkzeug.utils import secure_filename
from flask import request, current_app, g
from flask_restful import Resource

from app.models import Permission
from app.api_v1 import token_auth, HTTPStatusCodeMixin
from app.api_v1.decorators import permission_required
from app.api_v1.error import FileError
from app.utils.tools import allowed_file


class Upload(Resource, HTTPStatusCodeMixin):
    @token_auth.login_required
    @permission_required(Permission.ADMINISTER)
    def post(self):
        app = current_app._get_current_object()

        if 'file' not in request.file:
            raise FileError("upload file not exist")

        file = request.file['file']
        if file.filename == '':
            raise FileError("No selected file")

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            # 待转换成webp
            file.save(
                os.path.join(app.config['UPLOADED_PHOTOS_DEST'],
                             g.current_user.username, filename))
        return {}, self.CREATED
