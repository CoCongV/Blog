from flask import g, request

from app.api_v1 import BaseResource, token_auth
from app.models import Permission, Post


class PostPermission(BaseResource):
    decorators = [token_auth.login_required]

    def get(self):
        post_id = request.args.get('post_id')
        post = Post.query.get(post_id)
        if g.current_user == post.author or g.current_user.can(Permission.ADMINISTER):
            return {}, self.SUCCESS
        return {}, self.PERMISSION_FORBIDDEN
