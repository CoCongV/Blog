from datetime import datetime

import bleach
from markdown import markdown
from sqlalchemy.orm import relationship

from blog import db


class Reply(db.Model):
    __tablename__ = 'reply'
    reply_id = db.Column(
        db.Integer, db.ForeignKey('comments.id'), primary_key=True)
    replied_id = db.Column(db.Integer, db.ForeignKey('comments.id'))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow())


class Comment(db.Model):
    __tablename__ = 'comment'
    body = db.Column(db.String(1000))
    body_html = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=lambda: datetime.utcnow())
    disabled = db.Column(db.Boolean, default=False)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'))
    replied = relationship('Reply',
                              foreign_keys=[Reply.reply_id],
                              backref=db.backref('replies', lazy='joined'),
                              lazy='dynamic',
                              cascade='all, delete-orphan')
    replies = relationship('Reply',
                              foreign_keys=[Reply.replied_id],
                              backref=db.backref('replied', lazy='joined'),
                              lazy='dynamic',
                              cascade='all, delete-orphan')

    async def replay(self, comment):
        await Reply.create(replies=self, replied=comment)

    @staticmethod
    def on_change_body(target, value, oldvalue, initiator):
        allowed_tags = [
            'a', 'abbr', 'acronym', 'b', 'code', 'em', 'i', 'blockquote'
            'strong', 'ol', 'li', 'ul', 'p', 'span', 'img', 'pre', 's'
        ]
        allowed_styles = ['background-color']
        allowed_attributes = {'a': ['href', 'title'],
                              'abbr': ['title'],
                              'acronym': ['title'],
                              'pre': ['class', 'spellcheck']}
        target.body_html = bleach.linkify(
            bleach.clean(
                markdown(value, output_format='html'),
                tags=allowed_tags,
                strip=True,
                styles=allowed_styles,
                attributes=allowed_attributes))

    async def to_dict(self):
        data = {
            'body_html': self.body_html,
            'timestamp': self.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
            'author': self.author.username,
            'avatar': self.author.avatar
        }
        return data

db.event.listen(Comment.body, 'set', Comment.on_change_body)
