from flask import g, request, current_app, url_for
from flask_restful import Resource, reqparse

from blog import db
from blog.api_v1 import token_auth
from blog.api_v1.decorators import permission_required
from blog.models import Post, Comment, Permission

comment_parse = reqparse.RequestParser()
comment_parse.add_argument('body', location='json')
comment_parse.add_argument(
    'reply',
    location='json',
)
comment_parse.add_argument('post_id', required=True)
comment_parse.add_argument('page', type=int, default=1)


class CommentView(Resource):

    method_decorators = {
        'post':
        [permission_required(Permission.COMMENT), token_auth.login_required]
    }

    def post(self):
        args = comment_parse.parse_args()
        post = Post.get(args.post_id)
        comment = Comment.create(
            body=args.body, author=g.current_user, post=post)
        if args.comment_id:
            reply = Comment.query.get(args.comment_id)
            comment.reply(reply)
        return {}, 201

    def get(self):
        # 评论增加Email验证权限
        # 获取评论
        prev = None
        next_ = None
        args = comment_parse.parse_args()
        post = Post.query.get(args['post_id'])
        pagination = post.comments.order_by(db.desc('timestamp')).paginate(
            args.page, per_page=current_app.config['BLOG_COMMENT_PAGE'],
            error_out=False
        )
        comments = pagination.items
        if pagination.has_prev:
            prev = url_for('comment.commentview', page=args.page - 1, post=post.id)
        if pagination.has_next:
            next_ = url_for('comment.commentview', page=args.page + 1, post=post.id)
        return {
            'comments': [i.to_json() for i in comments],
            'prev': prev,
            'next': next_,
            'count': pagination.total
        }
