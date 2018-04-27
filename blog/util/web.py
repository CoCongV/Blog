from sanic import Blueprint
from sanic.request import File


class NestedBlueprint(Blueprint):

    def register_blueprint(self, bp):
        if not getattr(self, 'blueprints', None):
            self.blueprints = list()
        self.blueprints.append(bp)

    def register(self, app, options):
        super().register(app, options)
        for bp in self.blueprints:
            bp.name = '.'.join((self.name, bp.name))
            bp.url_prefix = ''.join((self.url_prefix, bp.url_prefix))
            bp.register(app, options)
