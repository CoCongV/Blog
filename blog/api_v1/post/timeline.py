from sqlalchemy import extract
from sqlalchemy.orm import sessionmaker
from flask_restful import Resource
from blog.models import Post
from blog import db


class Timeline(Resource):

    def get(self):
        _Session = sessionmaker(db.engine)
        session = _Session()
        results = set(session.query(extract('year', Post.timestamp)).all())
        return {'time': tuple(results)}
