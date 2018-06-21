from sanic_restful import Resource, reqparse

from blog.decorators import login_requred

from blog.models import User, Permission


parser = reqparse.RequestParser()
parser.add_argument('uid')


class UserProfile(Resource):

    method_decorators = [login_requred]

    async def get(self, request):
        args = parser.parse_args(request)
        current_user = request['current_user']
        user = await User.get(args.uid)
        edit_permission = True if current_user == user\
            or current_user.can(Permission.ADMINISTER) else False
        return {
            "user": user.to_json(),
            "edit_permission": edit_permission
        }
