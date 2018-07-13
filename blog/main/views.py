# coding: utf-8
import os

from flask import (render_template,
                   send_from_directory,
                   current_app,
                   send_file)

from blog.exceptions import FileError

from . import main
from .. import cache


@cache.cached(timeout=50)
@main.route('/')
def index():
    return render_template('index.html')


default_query = '''
{
    allPosts {
        edges {
            node {
                id,
                name,
                posts {
                    id,
                    title,
                    body
                }
            }
        }
    }
}'''.strip()


@main.route('/favicon.ico', methods=['GET'])
def favicon():
    return send_from_directory(
        os.path.join(current_app.root_path, 'static'),
        'favicon.ico',
        mimetype='image/vnd.microsoft.icon')


@main.route('/images/<uid>/<image>', methods=['GET'])
def image(uid, image):
    path = os.path.join(current_app.config['UPLOADED_PHOTOS_DEST'],
                        str(uid), image)
    if not os.path.exists(path):
        raise FileError()
    return send_file(path)
