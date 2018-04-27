from sanic.exceptions import Unauthorized
from sanic_restful import Resource, reqparse

from blog.decorators import login_requred
from blog.models import User


parser = reqparse.RequestParser()
parser.add_argument('email', required=True)
parser.add_argument('password', required=True)


class Login(Resource):

    async def post(self, request):
        args = parser.parse_args(request)
        user = await User.query.where(User.email == args.email).first()

        if not user:
            raise Unauthorized('Unauthorized')
        elif not user.verify_password(args.password):
            raise Unauthorized('Unauthorized')
        else:
            return {
                'token':
                user.generate_confirm_token(request.app.config.SECRET_KEY),
                'username': user.username,
                'permission': user.role.permission
            }

    async def delete(self, request):
        pass
