from base64 import b64encode

from flask_restful import Resource

from blog import flask_captchap


class ImageCaptcha(Resource):

    def get(self):
        img = flask_captchap.generate_img()
        # data = b64encode(img)
        return img
