from base64 import b64encode
from io import BytesIO

from flask import make_response, session, send_file
from flask.views import MethodView

from blog import flask_captcha


class ImageCaptcha(MethodView):

    def get(self):
        data, chars = flask_captcha.generate_img()
        session['captcha_code'] = chars
        return send_file(data, mimetype='image/png')
