from sqlalchemy import extract
from sqlalchemy.orm import sessionmaker
from flask_restful import Resource

from app.utils.web import HTTPStatusCodeMixin
from app.models import Post
from app import db, cache


class Timeline(Resource, HTTPStatusCodeMixin):

    @cache.cached(timeout=300)
    def get(self):
        _Session = sessionmaker(db.engine)
        session = _Session()
        results = tuple(set(session.query(extract('year', Post.timestamp)).all()))
        return {'time': results}, self.SUCCESS
