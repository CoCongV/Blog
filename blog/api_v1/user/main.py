import asyncio

from email.mime.text import MIMEText
from sanic.exceptions import Forbidden
from sanic_restful import Resource, reqparse
from sqlalchemy.exc import IntegrityError, InvalidRequestError

from blog import jinja_env
from blog.decorators import login_requred
from blog.exc import UserAlreadyExistsException
from blog.models import User, Role
from blog.util.email import send_eamil


parser = reqparse.RequestParser()
parser.add_argument('email', type=str, required=True, location='json')
parser.add_argument('username', type=str, required=True, location='json')
parser.add_argument('location', type=str, location='json')
parser.add_argument('about_me', type=str, location='json')
parser.add_argument('password', type=str, required=True, location='json')

reqparse_patch = reqparse.RequestParser()
reqparse_patch.add_argument(
    'email', type=str, location='json', store_missing=False)
reqparse_patch.add_argument(
    'username', type=str, location='json', store_missing=False)
reqparse_patch.add_argument(
    'location', type=str, location='json', store_missing=False)
reqparse_patch.add_argument(
    'about_me', type=str, location='json', store_missing=False)
reqparse_patch.add_argument(
    'password', type=str, location='json', store_missing=False)


class UserResouce(Resource):
    method_decorators = {
        'get': [login_requred],
        'patch': [login_requred]
    }

    async def get(self, request):
        user = request['current_user']
        if not user.is_anonymous:
            json_user = user.to_json()
            return json_user
        return {'username': ''}

    async def post(self, request):
        args = parser.parse_args(request)
        try:
            role = await Role.query.where(Role.permissions == 2).gino.first()
            user = await User.create(email=args.email,
                                     username=args.username,
                                     password=args.password,
                                     location=args.location,
                                     about_me=args.about_me,
                                     role=role)
        except (IntegrityError, InvalidRequestError):
            raise UserAlreadyExistsException()

        token = user.generate_confirm_token(request.app.config.SECRET_KEY)
        email_token = user.generate_email_token(request.app.config.SECRET_KEY)

        template = jinja_env.get_template('mail/confirm')
        rendered_template = await template.render_async(
            user=user.username,
            url=request.app.url_for(
                'auth.email_auth', token=email_token, _external=True))

        asyncio.ensure_future(
            send_eamil(request.app, user.email, 'Confirm Your Account',
                       rendered_template))
        return {
            'token': token,
            'permission': user.role.permission
        }

    async def patch(self, request):
        args = reqparse_patch.parse_args(request)
        request['current_user'].update(**args).apply()
        return {}, 204
