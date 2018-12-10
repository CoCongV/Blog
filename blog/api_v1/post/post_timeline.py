from sqlalchemy import extract

from flask import current_app, url_for
from flask_restful import reqparse, Resource

from blog import db
from blog.models import Post

parse = reqparse.RequestParser()
parse.add_argument('year', location='args')
parse.add_argument('page', location='args', type=int, default=1)


class PostTimeLine(Resource):

    def get(self):
        prev = None
        next_ = None
        args = parse.parse_args()
        year = args.year
        page = args.page
        per_page = current_app.config['BLOG_POST_PER_PAGE']

        pagination = Post.query.filter(
            extract('year', Post.timestamp) == year, Post.draft == False) \
            .order_by(db.desc(Post.timestamp)) \
            .paginate(page, per_page=per_page, error_out=False)

        posts = pagination.items
        if pagination.has_prev:
            prev = url_for(
                'post.post_time_line', page=page - 1, _external=True)
        if pagination.has_next:
            next_ = url_for(
                'post.post_time_line', page=page + 1, _external=True)

        return {
            'posts': [i.to_json(True) for i in posts],
            'prev': prev,
            'next': next_,
            'count': pagination.total
        }
