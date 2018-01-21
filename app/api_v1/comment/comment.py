from flask import g, request, current_app, url_for
from flask_restful import Resource, reqparse

from app import db
from app.api_v1 import token_auth
from app.api_v1.decorators import permission_required
from app.models import Post, Comment, Permission
from app.utils.celery.email import send_email

comment_parse = reqparse.RequestParser()
comment_parse.add_argument(
    'body',
    location='json',
    required=True
)
comment_parse.add_argument(
    'reply',
    location='json',
    required=False
)
comment_parse.add_argument(
    'post_id',
    location='json',
    required=True,
    type=int
)
comment_parse.add_argument('comment_id', location='json', type=int)


class CommentApi(Resource):

    method_decorators = {
        'post':
        [token_auth.login_required,
         permission_required(Permission.USER)]
    }

    def post(self):
        args = comment_parse.parse_args()
        post = Post.get(args.post_id)
        email = Post.author.email
        reply = Comment.create(
            body=args.body, author=g.current_user, post=post)
        if args.comment_id:
            comment = Comment.query.get_or_404(args.comment_id)
            comment.replies.append(reply)
            email = comment.author.email
            comment.save()
        send_email.delay(
            to=email,
            subject='View The Comment Detail',
            template='main/comment',
            url=url_for(
                'post.post_view', post_id=args.post_id, _external=True))
        return {}, 201

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
