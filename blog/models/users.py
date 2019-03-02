# coding: utf-8
from datetime import datetime

from flask import current_app
from flask_login import UserMixin, AnonymousUserMixin
from itsdangerous import TimedJSONWebSignatureSerializer
from werkzeug.security import generate_password_hash, check_password_hash

from blog import db, login_manager
from blog.models.minixs import CRUDMixin, Serializer
from .roles import Permission


class User(CRUDMixin, UserMixin, db.Model, Serializer):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), index=True, unique=True)
    username = db.Column(db.String(32), index=True, unique=True)
    avatar = db.Column(db.Text, default='static/img/images.png')
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    password_hash = db.Column(db.String(256))
    confirmed = db.Column(db.Boolean, default=False)
    location = db.Column(db.String(64))
    about_me = db.Column(db.String(128))
    member_since = db.Column(db.DateTime, default=lambda: datetime.utcnow())
    last_seen = db.Column(db.DateTime, default=lambda: datetime.utcnow())
    kindle_email = db.Column(db.String(64))

    posts = db.relationship('Post', backref='author', lazy='dynamic')
    comments = db.relationship(
        'Comment',
        backref='author',
        lazy='dynamic',
        cascade='all, delete-orphan')
    books = db.relationship('Book', back_populates='creater')

    def __repr__(self):
        return str(self.json()).replace(',', '\n')

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def generate_confirm_token(self, expiration=3600):
        """generate token for Email , reset password and verify password"""
        s = TimedJSONWebSignatureSerializer(
            current_app.config['SECRET_KEY'], expires_in=expiration)
        token = s.dumps({'confirm_id': self.id})
        return str(token, encoding='utf8')

    @staticmethod
    def verify_auth_token(token):
        s = TimedJSONWebSignatureSerializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except Exception as e:
            return False
        else:
            return User.query.get(data['confirm_id'])

    def generate_email_token(self, expiration=None):
        if not expiration:
            current_app.config['LOGIN_TOKEN']
        s = TimedJSONWebSignatureSerializer(
            current_app.config['SECRET_KEY'], expires_in=expiration)
        token = s.dumps({'email': self.email})
        return str(token, encoding='utf-8')

    @staticmethod
    def verify_email_token(token):
        s = TimedJSONWebSignatureSerializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except Exception as e:
            return False
        user = User.query.filter_by(email=data.get('email')).first()
        if not user:
            return False
        user.confirmed = True
        db.session.add(user)
        db.session.commit()
        return True

    def generate_reset_token(self, expiration=3600):
        s = TimedJSONWebSignatureSerializer(current_app.config['SECRET_KEY'],
                                            expiration)
        return s.dumps({'reset': self.id})

    def verify_reset_token(self, token, new_password):
        s = TimedJSONWebSignatureSerializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except Exception:
            return False
        if data.get('confirm_id') != self.id:
            return False
        self.password = new_password
        db.session.add(self)
        db.session.commit()
        return True

    def generate_change_mail_token(self, new_email, expiration=3600):
        s = TimedJSONWebSignatureSerializer(
            current_app.config['SECRET_KEY'], expires_in=expiration)
        return s.dumps({'change_mail': self.id, 'new_email': new_email})

    def verify_change_mail(self, token):
        s = TimedJSONWebSignatureSerializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except Exception:
            return False
        if data.get('change_mail') != self.id:
            return False
        new_email = data.get('new_email')
        if new_email is None:
            return False
        if self.query.filter_by(email=new_email).first() is not None:
            return False
        self.email = new_email
        db.session.add(self)
        db.session.commit()

    def can(self, permissions):
        return self.role is not None and self.role.has_permission(permissions)

    def is_administrator(self):
        return self.can(Permission.ADMINISTER)

    def ping(self):
        self.last_seen = datetime.utcnow()
        db.session.add(self)
        db.session.commit()

    def to_json(self):
        json_data = {
            "uid": self.id,
            "email": self.email,
            "username": self.username,
            "avatar": self.avatar,
            "location": self.location,
            "about_me": self.about_me,
            "last_seen": self.last_seen.strftime('%Y-%m-%d %H:%M'),
            "member_since": self.member_since.strftime('%Y-%m-%d %H:%M'),
            "confirmed": self.confirmed,
            "permission": self.role.permissions,
        }
        return json_data


class AnonymousUser(AnonymousUserMixin):
    @staticmethod
    def can(permissions):
        return False

    @staticmethod
    def is_administrator():
        return False

    def is_anonymous(self):
        return True


login_manager.anonymous_user = AnonymousUser


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
