from flask import g, request, current_app, url_for
from flask_restful import Resource
from markdown import markdown

from app import db
from app.api_v1 import HTTPStatusCode, token_auth, permission_required
from app.models import Post, Comment, Permission
from . import comment_parse


class CommentView(Resource, HTTPStatusCode):

    @token_auth.login_required
    @permission_required(Permission.COMMENT)
    def post(self):
        args = comment_parse.parse_args()
        reply = args.get('reply')
        post = Post.get(args['post'])
        kwargs = {'body': args['body'],
                  'author': g.current_user,
                  'post': post}
        if reply:
            kwargs.update({'replies': Comment.get(reply)})
        Comment.create(**kwargs)
        return self.CREATED

    def get(self):
        # 评论增加Email验证权限
        # 获取评论
        post = Post.query.get(request.args['post_id'])
        page = int(request.args.get('page', 1))
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
        }, self.SUCCESS
