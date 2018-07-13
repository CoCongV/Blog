from sqlalchemy import extract
from sqlalchemy.orm import sessionmaker
from flask_restful import Resource

from blog.utils.web import HTTPStatusCodeMixin
from blog.models import Post
from blog import db, cache


class Timeline(Resource, HTTPStatusCodeMixin):

    @cache.cached(timeout=86400)
    def get(self):
        _Session = sessionmaker(db.engine)
        session = _Session()
        results = set(session.query(extract('year', Post.timestamp)).all())
        return {'time': tuple(results)}, self.SUCCESS
