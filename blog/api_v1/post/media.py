import os

from sanic_restful import Resource, reqparse
from werkzeug.datastructures import FileStorage

from blog import photo
from blog.models import Permission
from blog.decorators import login_requred, permission_reuired

parser = reqparse.RequestParser()
parser.add_argument('image', location='file', type=FileStorage, required=True)


class PhotoStorage(Resource):
    decorators = [permission_reuired(Permission.ADMINISTER), login_requred]

    async def put(self, request):
        params = parser.parse_args(request)
        path = request.app.config.POST_IMAGE
        if os.path.exists(os.path.join(path, 'image', params.image.name)):
            file_url = photo.url(params.avatar.name)
        else:
            filepath = photo.save(params.image, 'image')
            file_url = photo.url(filepath)
        return {'url': file_url}
