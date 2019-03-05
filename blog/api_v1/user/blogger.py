from flask_restful import Resource

from blog.models import User, Role


class Blogger(Resource):
    def get(self):
        blogger = User.query.filter(Role.name == "Administrator").first()
        return {
            'username': blogger.username,
            'avatar': blogger.avatar,
            'about_me': blogger.about_me,
            'uid': blogger.id,
        }
