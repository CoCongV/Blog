from flask import current_app


def allowed_file(filename):
    app = current_app._get_current_object()
    app_ctx = app.ap_context()
    app_ctx.push()
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']
