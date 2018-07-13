from datetime import datetime

import bleach
from whoosh.analysis import SimpleAnalyzer

from markdown import markdown
from sqlalchemy import event
from sqlalchemy.dialects import postgresql
from sqlalchemy.orm import relationship

from blog import db


class Post(db.Model):
    __tablename__ = 'post'
    __searchable__ = ['body', 'title']
    __analyzer__ = SimpleAnalyzer()
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(32), index=True)
    body = db.Column(db.Text)
    body_html = db.Column(db.Text)
    timestamp = db.Column(
        db.DateTime, default=lambda: datetime.utcnow(), index=True)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    comments = relationship(
        'Comment',
        backref='post',
        lazy='dynamic',
        cascade='all, delete-orphan')
    tags = db.Column(postgresql.ARRAY(db.String(32)))
    view = db.Column(db.Integer, default=0)

    @staticmethod
    def on_change_body(target, value, oldvalue, initiator):
        target.body_html = bleach.linkify(
            markdown(value, output_format='html'))

    async def to_dict(self, app, split=False):
        data = {
            "post_id": self.id,
            'tags': self.tags,
            "url": app.url_for('post.postview', post_id=self.id),
            "title": self.title,
            'timestamp': self.timestamp.strftime('%Y-%m-%d %H:%M'),
            'author': self.author.username,
            'avatar': self.author.avatar,
            'view': self.view
        }
        if split:
            data.update({'body_html': self.body_html[:500]})
        else:
            data.update({
                'body_html':
                self.body_html,
                'body':
                self.body,
                'author_url':
                app.url_for('user.user_profile', uid=self.author_id)
            })
        return data

    @staticmethod
    async def generate_fake(count=100):
        from random import seed, randint
        import forgery_py

        seed()
        for i in range(count):
            await Post.create(
                title='测试',
                body=forgery_py.lorem_ipsum.sentences(randint(1, 3)),
                author_id=1,
                tags=['测试']
            )


# event.listen(Post.body, 'set', Post.on_change_body)
