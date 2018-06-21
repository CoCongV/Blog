from sanic.
from sanic_restful import Resource, reqparse

from blog.decorators import login_requred, permission_reuired
from blog.models import Post, Comment
from blog.util.page import paginate


parser = reqparse.RequestParser()
parser.add_argument('body', required=True)
parser.add_argument('reply')
parser.add_argument('post_id', required=True)
parser.add_argument('comment_id')
parse.add_argument('page', default=1)


class CommentApi(Resource):
    method_decorators = {
        'post': [permission_reuired, login_requred]
    }

    async def post(self, request):
        params = parser.parse_args(request)
        post = await Post.get(params.post_id)
        comment = await Comment.create(
            body=params.body, author=request['current_user'], post=post)
        if params.comment_id:
            replied = await Comment.get(params.comment_id)
            comment.reply(replied)
        return ''

    async def get(self, request):
        params = parser.parse_args(request)
        post = await Post.get(params.post_id)
        per_page = request.app.config.get('BLOG_COMMENT_PAGE', 20)
        query = post.comments.order_by(Post.timestamp.desc())
        pagination = paginate(query, params.page, per_page)
        comments = pagination.items
        prev = request.app.url_for(
            'comment.commentapi', page=page - 1, post_id=post.id) \
            if pagination.has_prev else None
        next_ = request.app.url_for(
            'comment.commentapi', page=page + 1, post_id=post.id) \
            if pagination.has_next else None
        return {
            'comments': [i.to_dict() for i in comments],
            'prev': prev,
            'next': next_,
            'count': pagination.total
        }
