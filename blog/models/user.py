from datetime import datetime

from itsdangerous import TimedJSONWebSignatureSerializer
from werkzeug.security import generate_password_hash, check_password_hash

from blog import db
from . import Permission


class User(db.Model):
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
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    comments = db.relationship(
        'Comment',
        backref='author',
        lazy='dynamic',
        cascade='all, delete-orphan')

    @property
    async def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    async def password(self, password):
        await self.update(password_hash=generate_password_hash(password)
                          ).apply()

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def generate_confirm_token(self, key, expiration=60 * 60):
        s = TimedJSONWebSignatureSerializer(key, expires_in=expiration)
        token = s.dumps({'uid': self.id})
        return str(token, encoding='utf8')

    @staticmethod
    async def verify_auth_token(key, token):
        s = TimedJSONWebSignatureSerializer(key)
        try:
            data = s.loads(token)
        except Exception:
            return False
        else:
            return await User.get(data['confirm_id'])

    async def generate_email_token(self, key, expiration=60 * 60):
        s = TimedJSONWebSignatureSerializer(
            key, expires_in=expiration, salt='email')
        token = s.dumps({'email': self.email})
        return str(token)

    @staticmethod
    async def verify_email_token(token, key):
        s = TimedJSONWebSignatureSerializer(key, salt='email')
        try:
            data = s.loads(token)
        except Exception:
            return False
        user = await User.get(data['uid'])
        if not user:
            return False
        await user.update(confirmed=True).apply()
        return True

    async def generate_reset_token(self, key, expiration):
        s = TimedJSONWebSignatureSerializer(key, expiration)
        return s.dumps({'reset': self.id})

    async def verify_reset_token(self, key, token, new_password):
        s = TimedJSONWebSignatureSerializer(key)
        try:
            data = s.loads(token)
        except Exception:
            return False
        if data.get('reset') != self.id:
            return False
        self.password = new_password

    async def generate_change_email_token(self,
                                          new_email,
                                          token,
                                          key,
                                          expiration=60 * 60):
        s = TimedJSONWebSignatureSerializer(key, expires_in=expiration)
        return s.dumps({'change_email': self.id, 'new_email': new_email})

    async def verify_change_email(self, key, token):
        s = TimedJSONWebSignatureSerializer(key)
        try:
            data = s.loads(token)
        except Exception:
            return False
        if data.get('change_email') != self.id:
            return False
        new_email = data.get('new_email')
        if new_email is None:
            return False
        user = await User.query.where(User.email == new_email).gino.first()
        if user:
            return False
        await self.update(email=new_email).apply()
        return True

    def can(self, permission):
        return self.role is not None and (
            self.role.permissions & permission) == permission

    def is_administrator(self):
        return self.can(Permission.ADMINISTER)

    async def ping(self):
        await self.update(last_seen=datetime.utcnow())

    def to_dict(self):
        data = {
            'uid': self.id,
            'email': self.email,
            'username': self.username,
            'avatar': self.avatar,
            'location': self.location,
            'about_me': self.about_me,
            'last_seen': self.last_seen,
            'member_since': self.member_since,
            'confirmed': self.confirmed
        }
        return data
