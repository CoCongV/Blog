from base64 import b64encode

from flask import make_response
from flask.views import MethodView

from blog import flask_captchap


class ImageCaptcha(MethodView):

    def get(self):
        img = flask_captchap.generate_img()
        # data = b64encode(img)
        rep = make_response(img)
        return rep
