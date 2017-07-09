from flask import g, url_for
from flask_restful import request, reqparse, Resource

from app.models import Post, Permission
from app.api_v1 import HTTPStatusCode, token_auth
from app.api_v1.decorators import permission_required

post_parser = reqparse.RequestParser()
post_parser.add_argument(
    'title',
    location='json',
    required=True
)
post_parser.add_argument(
    'content',
    location='json',
    required=True
)
post_parser.add_argument(
    'tags',
    location='json',
    action='append',
    required=True
)


class PostView(Resource, HTTPStatusCode):

    decorators = [token_auth.login_required]

    @permission_required(Permission.ADMINISTER)
    def post(self):
        # 新建文章
        args = post_parser.parse_args()
        title = args['title']
        body = args['content']
        tags = args['tags']

        author = g.current_user
        post = Post.create(title=title, body=body, tags=tags, author=author)
        return {'url': url_for('post.postview', id=post.id), 'id': post.id}, self.CREATED

    def get(self):
        # 认证权限与请求文章分离
        _delete = True
        post = Post.get_or_404(request.args.get('id')).update(view=Post.view + 1)
        if not g.current_user.can(Permission.ADMINISTER) and g.current_user != post.author:
            _delete = False
        return {"post": post.to_json(),
                'delete_permission': _delete}, self.SUCCESS

    @permission_required(Permission.ADMINISTER)
    def put(self):
        # 修改文章
        args = post_parser.parse_args()
        title = args['title']
        body = args['content']
        tags = args['tags']
        post = Post.get(args['post_id'])
        if g.current_user != post.author and not g.current_user.can(Permission.ADMINISTER):
            return {"message": "Insufficient permissions"}, self.PERMISSION_FORBIDDEN
        post.body = body
        post.title = title
        post.tags = tags
        post.save()
        return {'url': url_for('post.postview', id=post.id), 'post_id': post.id}, self.SUCCESS

    @permission_required(Permission.ADMINISTER)
    def delete(self):
        post = Post.get_or_404(request.args['post_id'])
        if g.current_user != post.author and not g.current_user.can(Permission.ADMINISTER):
            return {"message": "Insufficient permissions"}, self.PERMISSION_FORBIDDEN
        post.delete()
        return {}, self.SUCCESS
