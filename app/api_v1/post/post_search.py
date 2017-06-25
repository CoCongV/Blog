from sqlalchemy import extract
from sqlalchemy.orm import sessionmaker

from flask_restful import reqparse

from app import db
from app.api_v1 import BaseResource
from app.models import Post


search_parse = reqparse.RequestParser()
search_parse.add_argument('tag', location='args')
search_parse.add_argument('year', location='args')
search_parse.add_argument('search', location='args')


class PostSearch(BaseResource):

    def get(self):
        _Session = sessionmaker(db.engine)
        session = _Session()
        args = search_parse.parse_args()
        tag = args.get('tag')
        year = args.get('year')
        content = args.get('search')
        print(content)
        if tag:
            posts = session.query(Post)\
                .filter(Post.tags.any(tag))\
                .order_by(db.desc(Post.timestamp))
        elif year:
            posts = session.query(Post)\
                .filter(extract('year', Post.timestamp) == year)\
                .order_by(db.desc(Post.timestamp))
        elif content:
            posts = Post.query.whoosh_search(content).order_by(db.desc(Post.timestamp)).all()
        else:
            posts = []
        return {
                   'posts': [i.to_json(True) for i in posts]
               }, self.SUCCESS
