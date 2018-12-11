from base64 import b64encode
from io import BytesIO

from flask import make_response, session, send_file, current_app
from flask.views import MethodView

from blog.utils import FlaskCaptcha


class ImageCaptcha(MethodView):

    def get(self):
        captch = FlaskCaptcha()
        captch.init_app(current_app)
        data, chars = captch.generate_img()
        session['captcha_code'] = chars
        return send_file(data, mimetype='image/png')
