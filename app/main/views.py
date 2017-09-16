# coding: utf-8
import os

from flask import render_template, send_from_directory, current_app

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


@main.route('/favicon.ico')
def favicon():
    print(current_app.root_path)
    return send_from_directory(
        os.path.join(current_app.root_path, 'static'),
        'favicon.ico',
        mimetype='image/vnd.microsoft.icon')
