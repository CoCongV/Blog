from sqlalchemy import extract

from flask import current_app, url_for
from flask_restful import reqparse, Resource

from app import db, cache
from app.utils.web import HTTPStatusCodeMixin
from app.models import Post

_parse = reqparse.RequestParser()
_parse.add_argument('year', location='args')
_parse.add_argument('page', location='args')


class PostTimeLine(Resource, HTTPStatusCodeMixin):

    @cache.cached(1800)
    def get(self):
        args = _parse.parse_args()
        year = args['year']
        page = args.get('page', 1)
        pagination = Post.query.filter(extract('year', Post.timestamp) == year) \
            .order_by(db.desc(Post.timestamp)) \
            .paginate(
            page, per_page=current_app.config['BLOG_POST_PER_PAGE'],
            error_out=False
        )
        posts = pagination.items
        prev = None
        if pagination.has_prev:
            prev = url_for(
                'post.post_time_line', page=page - 1, _external=True)
        _next = None
        if pagination.has_next:
            _next = url_for(
                'post.post_time_line', page=page + 1, _external=True)

        return {
            'posts': [i.to_json(True) for i in posts],
            'prev': prev,
            'next': _next,
            'count': pagination.total
        }, self.SUCCESS
