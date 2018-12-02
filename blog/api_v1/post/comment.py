from flask import g, request, current_app, url_for
from flask_restful import Resource, reqparse

from blog import db
from blog.api_v1 import token_auth
from blog.api_v1.decorators import permission_required
from blog.models import Post, Comment, Permission

comment_parse = reqparse.RequestParser()
comment_parse.add_argument('body', location='json')
comment_parse.add_argument('page', type=int, default=1)
comment_parse.add_argument('comment_id', type=int)


class CommentsView(Resource):

    method_decorators = {
        'post':
        [permission_required(Permission.COMMENT), token_auth.login_required]
    }

    def post(self, post_id):
        args = comment_parse.parse_args()
        comment_id = args.comment_id
        post = Post.get(post_id)
        comment = Comment.create(
            body=args.body, author=g.current_user, post=post)
        if comment_id:
            reply = Comment.query.get(comment_id)
            comment.reply(reply)
        return {}, 201

    def get(self, post_id):
        # 评论增加Email验证权限
        # 获取评论
        args = comment_parse.parse_args()
        post = Post.query.get(post_id)
        page = args.page
        pagination = post.comments.order_by(db.desc('timestamp')).paginate(
            page, per_page=current_app.config['BLOG_COMMENT_PAGE'],
            error_out=False
        )
        comments = pagination.items
        prev = None
        if pagination.has_prev:
            prev = url_for('comment.commentview', page=page - 1, post=post.id)
        _next = None
        if pagination.has_next:
            _next = url_for('comment.commentview', page=page + 1, post=post.id)
        return {
            'comments': [i.to_json() for i in comments],
            'prev': prev,
            'next': _next,
            'count': pagination.total
        }
