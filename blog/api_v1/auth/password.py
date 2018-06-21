from sanic.exceptions import Unauthorized
from sanic_restful import reqparse, Resource

from blog.decorators import permission_reuired, login_requred
from blog.models import Permission

parser = reqparse.RequestParser()
parser.add_argument('old_password', location='json', required=True)
parser.add_argument('new_password', location='json', required=True)


class Password(Resource):

    decorators = [permission_reuired(Permission.COMMENT), login_requred]

    async def patch(self, request):
        user = request['current_user']
        args = parser.parse_args(request)
        verify = await user.verify_password(args.old_password)
        if not verify:
            raise Unauthorized('Old Password Error')
        await user.update(password=args.new_password).apply()
        return '', 204
