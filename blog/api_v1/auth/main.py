import asyncio

from sanic.exceptions import Unauthorized
from sanic.response import redirect
from sanic_restful import Resource, reqparse

from blog import jinja_env
from blog.decorators import permission_reuired, login_requred
from blog.exc import UserAlreadyExistsException
from blog.models import User, Permission
from blog.util.email import send_eamil


class SendEmailAuth(Resource):

    decorators = [permission_reuired(Permission.COMMENT), login_requred]

    async def get(self, request):
        user = request['current_user']
        email_token = user.generate_email_token()
        template = jinja_env.get_template('mail/confirm')
        rendered_template = await template.render_async(
            user=user.username,
            url=request.app.url_for(
                'auth.email_auth', token=email_token, _external=True))
        asyncio.ensure_future(
            send_eamil(request.app, user.email, 'Confirm Your Account',
                       rendered_template))
        return ''


exist_parser = reqparse.RequestParser()
exist_parser.add_argument('email', type=str, location='args')
exist_parser.add_argument('username', type=str, location='args')


class UserExist(Resource):

    async def get(self, request):
        args = exist_parser.parse_args(request)
        user = await User.query.where(User.email == args.email).gino.first()
        if user:
            raise UserAlreadyExistsException()
        user = await User.query.where(User.username == args.username).gino.first()
        if user:
            raise UserAlreadyExistsException()
        else:
            return '', 204


class EmailAuth(Resource):

    async def get(self, request, token):
        result = await User.verify_email_token(token,
                                               request.app['SECRET_KEY'])
        if result:
            return redirect('/')
        else:
            raise Unauthorized('Email Verify Failure')
