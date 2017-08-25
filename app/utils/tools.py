from app import app


def allowed_file(filename):
    app.app_context().push()
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']
