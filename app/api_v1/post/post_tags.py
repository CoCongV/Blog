from flask import current_app, url_for
from flask_restful import reqparse, Resource

from app import db, cache
from app.utils.web import HTTPStatusCodeMixin
from app.models import Post


tag_parse = reqparse.RequestParser()
tag_parse.add_argument('tag', location='args')
tag_parse.add_argument('page', location='args')


class PostTags(Resource, HTTPStatusCodeMixin):

    @cache.cached(300)
    def get(self):
        prev = None

        args = tag_parse.parse_args()
        tag = args['tag']
        page = args.get('page', 1)

        pagination = Post.query.filter(Post.tags.any(tag)) \
            .order_by(db.desc(Post.timestamp)) \
            .paginate(
            page, per_page=current_app.config['BLOG_POST_PER_PAGE'],
            error_out=False
        )
        posts = pagination.items
        total = pagination.total
        if pagination.has_prev:
            prev = url_for('post.post_tags', page=page - 1, _external=True)
        _next = None
        if pagination.has_next:
            _next = url_for('post.post_tags', page=page + 1, _external=True)

        return {
            'posts': [i.to_json(True) for i in posts],
            'prev': prev,
            'next': _next,
            'count': total
        }, self.SUCCESS