from sanic_restful import Resource

from blog.decorators import login_requred


class Token(Resource):

    decorators = [login_requred]

    async def get(self, request):
        token = request['current_user'].generate_confirm_token(
            request.app.config.SECRET_KEY)
        return {'token': token}
