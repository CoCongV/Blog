from .captcha import FlaskCaptcha
from .session import RedisSessionInterface


class Single(type):
    def __init__(cls, *args, **kwargs):
        cls.__instance = None
        super(Single, cls).__init__(*args, **kwargs)

    def __call__(self, *args, **kwargs):
        if self.__instance is None:
            self.__instance = super(Single, self).__call__(*args, **kwargs)
            return self.__instance
        else:
            return self.__instance

    @classmethod
    def reload(mcs):
        mcs.__instance = None


__all__ = ['FlaskCaptcha', 'Single', ]
