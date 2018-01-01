from operator import itemgetter
from collections import deque

from sqlalchemy import func
from sqlalchemy.orm import sessionmaker
from flask_restful import Resource

from app import db, cache
from app.models import Post
from app.utils.web import HTTPStatusCodeMixin


class Tag(Resource, HTTPStatusCodeMixin):

    @cache.cached(timeout=1800)
    def get(self):
        _Session = sessionmaker(db.engine)
        session = _Session()
        result = session.query(
            Post.tags, func.count(Post.tags)).group_by(Post.tags).all()
        result.sort(key=itemgetter(1))
        tags = list(deque(set(l for i in result for l in i[0]), maxlen=10))
        return {"tags": tags}, self.SUCCESS