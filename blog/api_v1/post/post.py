from flask import g, url_for, current_app
from flask_restful import reqparse, Resource
from flask_restful.inputs import boolean
from werkzeug.exceptions import Forbidden, Unauthorized

from blog import db
from blog.models import Post, Permission
from blog.api_v1 import token_auth
from blog.api_v1.decorators import permission_required

post_parser = reqparse.RequestParser()
post_parser.add_argument('title', location='json', required=True)
post_parser.add_argument('content', location='json', required=True)
post_parser.add_argument(
    'tags', location='json', action='append', default=[])
post_parser.add_argument('post_id', location='json')
post_parser.add_argument('draft', default=False, type=boolean)


class PostView(Resource):

    method_decorators = {
        'patch': [
            permission_required(Permission.ADMINISTER, Unauthorized),
            token_auth.login_required
        ],
        'delete': [
            permission_required(Permission.ADMINISTER),
            token_auth.login_required
        ]
    }

    def get(self, post_id):
        post = Post.get_or_404(post_id).update(view=Post.view + 1)
        return {"post": post.to_json()}

    def patch(self, post_id):
        # 修改文章
        args = post_parser.parse_args()
        body = args.content
        post = Post.get_or_404(post_id)
        if g.current_user != post.author and not g.current_user.can(
                Permission.ADMINISTER):
            raise Forbidden(description="Insufficient permissions")
        post.update(
            title=args.title,
            body=args.content,
            tags=args.tags,
            draft=args.draft)
        return {
            'url': url_for('post.postview', post_id=post.id),
            'post_id': post.id
        }

    def delete(self, post_id):
        post = Post.get_or_404(post_id)
        if g.current_user != post.author and not g.current_user.can(
                Permission.ADMINISTER):
            raise Forbidden(description='Insufficient permissions')
        post.delete()
        return {}


posts_parser = reqparse.RequestParser()
posts_parser.add_argument('draft', default=False, type=boolean)
posts_parser.add_argument('page', type=int, default=1)


class PostsView(Resource):

    method_decorators = {
        'post': [
            permission_required(Permission.ADMINISTER),
            token_auth.login_required
        ],
        'get': [token_auth.login_required]
    }

    def get(self):
        args = posts_parser.parse_args()
        if args.draft:
            if not g.current_user.can(Permission.ADMINISTER):
                raise Forbidden()

        prev = None
        next_ = None
        per_page = current_app.config['BLOG_POST_PER_PAGE']
        post_query = Post.query.filter_by(draft=args.draft).order_by(
            db.desc('timestamp'))

        pagination = post_query.paginate(
            args.page, per_page=per_page, error_out=False)
        posts = pagination.items

        if pagination.has_prev:
            prev = url_for(
                'post.postsview', page=args.page - 1, _external=True)
        if pagination.has_next:
            next_ = url_for(
                'post.postsview', page=args.page + 1, _external=True)

        return {
            'posts': [post.to_json(500) for post in posts],
            'prev': prev,
            'next': next_,
            'count': pagination.total,
            'pages': pagination.pages,
        }

    def post(self):
        # 新建文章
        args = post_parser.parse_args(strict=True)

        author = g.current_user
        post = Post.create(
            title=args.title,
            body=args.content,
            tags=args.tags,
            author=author,
            draft=args.draft)
        return {
            'url': url_for('post.postview', post_id=post.id),
            'id': post.id
        }, 201
