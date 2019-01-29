from flask import current_app, url_for
from flask_restful import reqparse, Resource

from blog import db
from blog.models import Post


tag_parse = reqparse.RequestParser()
tag_parse.add_argument('tag', location='args')
tag_parse.add_argument('page', location='args', deafult=1, type=int)


class PostTags(Resource):

    def get(self):
        prev = None
        next_ = None
        args = tag_parse.parse_args()

        pagination = Post.query.filter(Post.tags.any(args.tag), Post.draft == False) \
            .order_by(db.desc(Post.timestamp)) \
            .paginate(
            args.page, per_page=current_app.config['BLOG_POST_PER_PAGE'],
            error_out=False
        )
        posts = pagination.items
        total = pagination.total

        if pagination.has_prev:
            prev = url_for(
                'post.post_tags', page=args.page - 1, _external=True)
        if pagination.has_next:
            next_ = url_for(
                'post.post_tags', page=args.page + 1, _external=True)

        return {
            'posts': [i.to_json(True) for i in posts],
            'prev': prev,
            'next': next_,
            'count': total
        }
