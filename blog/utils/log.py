import inspect
import logging
from logging.handlers import RotatingFileHandler, TimedRotatingFileHandler

from flask import current_app


_LOGFILE = current_app.config['_LOGFILE']
_MAX_LOG_SIZE = current_app.config['_MAX_LOG_SIZE']
_FORMAT = current_app.config['_FORMAT']
_formatter = current_app.config['_formatter']
_LOG_LEVEL = current_app.config['_LOG_LEVEL']


def decorete_emit(fn):
    """
        日志颜色输出控制：30: 黑色 31: 红色 32: 绿色 33: 黄色 34: 蓝色 35: 紫色 36: 深绿 37: 白色
        """

    def new(*args):
        levelno = args[0].levelno
        if levelno >= logging.CRITICAL:
            color = '\x1b[31;1m'
        elif levelno >= logging.ERROR:
            color = '\x1b[35;1m'
        elif levelno >= logging.WARNING:
            color = '\x1b[33;1m'
        elif levelno >= logging.INFO:
            color = '\x1b[36;1m'
        elif levelno >= logging.DEBUG:
            color = '\x1b[34;1m'
        else:
            color = '\x1b[0m'

        args[0].level = "{0}{1}\x1b[0m".format(color, args[0].level)

        return fn(*args)
    return new

# 普通日志文件
_file_handler = logging.FileHandler(_LOGFILE)
_file_handler.setFormatter(_formatter)

# 按大小循环分割日志文件
_rotate_file_handler = RotatingFileHandler(_LOGFILE, mode='a', maxBytes=_MAX_LOG_SIZE, backupCount=50)
_rotate_file_handler.setFormatter(_formatter)

# 按时间分割日志文件
_time_file_handler = TimedRotatingFileHandler(_LOGFILE, when='h', interval=6, backupCount=50)
_time_file_handler.setFormatter(_formatter)

# 标准输出
_console_handler = logging.StreamHandler()
_console_handler.setFormatter(_formatter)
_console_handler.emit = decorete_emit(_console_handler.emit)

# 根日志对象属性设置
_root_logger = logging.getLogger()
_root_logger.setLevel(_LOGFILE)
_root_logger.addHandler(_rotate_file_handler)
_root_logger.addHandler(_console_handler)


class Log(logging.RootLogger):
    """
    自定义日志类
    """
    def __init__(self, level=logging.DEBUG):
        logging.RootLogger.__init__(self, level=level)
        self.setLevel(level)
        self.addHandler(_rotate_file_handler)
        self.addHandler(_console_handler)

        self.DEBUG = logging.DEBUG
        self.INFO = logging.INFO
        self.WARNING = logging.WARNING
        self.ERROR = logging.ERROR
        self.CRITICAL = logging.CRITICAL

    def set_log(self, level):
        """
        设置日志等级
        """
        self.setLevel(level)

    @property
    def fun_name(self):
        """
        获取函数名
        """
        return inspect.stack()[1][3]
