import random

from captcha.image import ImageCaptcha
from flask import Flask


class FlaskCaptcha:
    CHAR = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'

    def init_app(self, app: Flask):
        self.fonts_path = app.config.get('CAPTCHA_FONTS_PATH') or None
        self.image_engine = ImageCaptcha(
            fonts=self.fonts_path) if self.fonts_path else ImageCaptcha()

    def generate_img(self):
        chars = ''.join(random.choices(self.CHAR, k=4))
        data = self.image_engine.generate(chars)
        return data, chars
