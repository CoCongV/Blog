from flask import Blueprint


class HTTPStatusCodeMixin(object):
    SUCCESS = 200
    CREATED = 201
    UNAUTHORIZED_ACCESS = 401
    PERMISSION_FORBIDDEN = 403
    USER_EXIST = 409  # 用户信息已被使用
    NOT_ALLOWED = 405

    def __init__(self):
        super(HTTPStatusCodeMixin, self).__init__()


class NestableBlueprint(Blueprint):
    """
    Hacking in support for nesting blueprints, until hopefully https://github.com/mitsuhiko/flask/issues/593 will be resolved
    """

    def register_blueprint(self, blueprint, **options):
        def deferred(state):
            url_prefix = (state.url_prefix or u"") + (options.get(
                'url_prefix', blueprint.url_prefix) or u"")
            if 'url_prefix' in options:
                del options['url_prefix']

            state.app.register_blueprint(
                blueprint, url_prefix=url_prefix, **options)

        self.record(deferred)