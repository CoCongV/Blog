from flask import g, request, current_app, url_for

from app.api_v1 import BaseResource, token_auth
from app.models import Post, Comment
from . import comment_parse


class CommentView(BaseResource):

    @token_auth.login_required
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
        post = Post.query.get(request.args['post'])
        page = request.args.get('page', 1)
        pagination = Comment.query.filter(post=post).order_by('-timestamp').paginate(
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
            'comments': [i.to_json for i in comments],
            'prev': prev,
            'next': _next,
            'count': pagination.total
        }
