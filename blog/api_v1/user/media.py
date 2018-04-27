import os

from sanic.request import File
from sanic_restful import Resource, reqparse

from blog import photo
from blog.decorators import login_requred, permission_reuired


parser = reqparse.RequestParser()
parser.add_argument('avatar', location='files', rquired=True, type=File)


class Avatar(Resource):

    decorators = [permission_reuired, login_requred]

    async def put(self, request, user):
        path = request.app.config.AVATAR_PATH
        args = parser.parse_args(request)
        if os.path.exists(
           os.path.join(path, 'avatar', args.avatar.name)):
            file_url = photo.url(args.avatar.name)
        else:
            filepath = photo.save(args.avatar, 'avatar')
            file_url = photo.url(filepath)
            await user.update(avatar=file_url)
        return {'url': file_url}, 201
