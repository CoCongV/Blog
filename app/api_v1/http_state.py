class HTTPStatusCodeMixin(object):
    SUCCESS = 200
    CREATED = 201
    UNAUTHORIZED_ACCESS = 401
    PERMISSION_FORBIDDEN = 403
    USER_EXIST = 409  # 用户信息已被使用

    def __init__(self):
        super(HTTPStatusCodeMixin, self).__init__()