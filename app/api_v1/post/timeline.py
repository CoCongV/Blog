from sqlalchemy import extract
from sqlalchemy.orm import sessionmaker

from app.api_v1 import BaseResource
from app.models import Post
from app import db


class Timeline(BaseResource):

    def get(self):
        _Session = sessionmaker(db.engine)
        session = _Session()
        results = tuple(set(session.query(extract('year', Post.timestamp)).all()))
        return {'time': results}, 200
