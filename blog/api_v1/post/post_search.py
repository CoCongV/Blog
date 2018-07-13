from sqlalchemy import extract

from flask import current_app, url_for
from flask_restful import reqparse, Resource

from blog import db
from blog.models import Post


search_parse = reqparse.RequestParser()
search_parse.add_argument('tag', location='args')
search_parse.add_argument('year', location='args')
search_parse.add_argument('search', location='args')
search_parse.add_argument('page', location='args', type=int, default=1)


class PostSearch(Resource):

    def get(self):
        prev = None
        _next = None
        total = 0
        per_page = current_app.config['BLOG_POST_PER_PAGE']

        args = search_parse.parse_args()
        tag = args.tag
        year = args.year
        content = args.search
        page = args.page
        if tag:
            pagination = Post.query.filter(Post.tags.any(tag))\
                .order_by(db.desc(Post.timestamp)) \
                .paginate(page, per_page=per_page, error_out=False)
        elif year:
            pagination = Post.query.filter(extract('year', Post.timestamp) == year)\
                .order_by(db.desc(Post.timestamp)) \
                .paginate(page, per_page=per_page, error_out=False)
        elif content:
            pagination = Post.query.whoosh_search(content)\
                .order_by(db.desc(Post.timestamp))\
                .paginate(page, per_page=per_page, error_out=False)
        else:
            pagination = None

        if pagination:
            posts = pagination.items
            total = pagination.total
            if pagination.has_prev:
                prev = url_for(
                    'post.post_search', page=page - 1, _external=True)
            if pagination.has_next:
                _next = url_for(
                    'post.post_search', page=page + 1, _external=True)
        else:
            posts = []
        return {'posts': [i.to_json(True) for i in posts],
                'prev': prev,
                'next': _next,
                'count': total}
