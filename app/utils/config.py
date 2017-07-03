from configparser import ConfigParser

from app.lib import Single


class Config(metaclass=Single):
    def __init__(self):
        self.cp = ConfigParser()
        with open('./config/config.ini', encoding='utf-8') as f:
            self.cp.read_file(f)
