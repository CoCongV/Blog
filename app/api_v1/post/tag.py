from operator import itemgetter
from collections import deque

from sqlalchemy import func
from sqlalchemy.orm import sessionmaker

from app.api_v1 import BaseResource
from app.models import Post
from app import db


class Tag(BaseResource):

    @staticmethod
    def get():
        _Session = sessionmaker(db.engine)
        session = _Session()
        result = session.query(Post.tags, func.count(Post.tags)).group_by(Post.tags).all()
        result.sort(key=itemgetter(1))
        tags = list(deque(set(l for i in result for l in i[0]), maxlen=10))
        return {"tags": tags}, 200
