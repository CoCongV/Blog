from sanic_restful import Resource, reqparse
from sqlalchemy import extract

from blog import db
from blog.models import Post


search_parse = reqparse.RequestParser()
search_parse.add_argument('tag')
search_parse.add_argument('year')
search_parse.add_argument('search')
search_parse.add_argument('page', type=int)


class PostSearch(Resource):

    async def get(self, request):
        params = search_parse.parse_args(request)
        query = await Post.query.where(
            Post.tags.any(params.tag),
            extract('year', Post.timestamp) == params.year)
