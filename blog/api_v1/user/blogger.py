from flask_restful import Resource

from blog.models import User, Role


class Blogger(Resource):
    def get(self):
        administrator = Role.query.filter_by(
            name="Administrator").first()
        blogger = User.query.filter_by(role=administrator).first()
        return {
            'username': blogger.username,
            'avatar': blogger.avatar,
            'about_me': blogger.about_me,
            'uid': blogger.id,
        }
