import random

from captcha.image import ImageCaptcha
from flask import Flask


class FlaskCaptcha:
    CHAR = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'

    def init_app(self, app: Flask):
        self.fonts_path = app.config['CAPTCHA_FONTS_PATH']
        self.image_engine = ImageCaptcha(self.fonts_path)
    
    def generate_img(self):
        chars = ''.join(random.choices(self.CHAR, k=4))
        data = self.image_engine.generate(chars)
        return data
    