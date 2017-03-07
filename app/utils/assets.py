from flask_assets import Environment, Bundle

css_all = Bundle('css/lib/*.css', filters='cssmin', output='css/all.min.css')
js_all = Bundle('js/lib/*.js', filters='jsmin', output='js/all.min.js')


def init_app(app):
    webassets = Environment(app)
    webassets.register('css.all', css_all)
    webassets.register('js_all', js_all)
    webassets.manifest = 'cache' if not app.debug else False
    webassets.cache = not app.debug
    webassets.debug = app.debug
