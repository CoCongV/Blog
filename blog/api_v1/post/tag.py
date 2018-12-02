from operator import itemgetter
from collections import deque

from sqlalchemy import func
from sqlalchemy.orm import sessionmaker
from flask_restful import Resource

from blog import db
from blog.models import Post


class Tag(Resource):

    def get(self):
        _Session = sessionmaker(db.engine)
        session = _Session()
        result = session.query(
            Post.tags, func.count(Post.tags)).group_by(Post.tags).all()
        result.sort(key=itemgetter(1))
        return {
            "tags": list(
                deque(set(l for i in result for l in i[0]), maxlen=10))
        }
