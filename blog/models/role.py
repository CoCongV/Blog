from blog import db

from sqlalchemy.orm import relationship


class Permission:
    COMMENT = 0x02
    ADMINISTER = 0xff


class Role(db.Model):
    __tablename__ = 'role'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    default = db.Column(db.Boolean, default=False, index=True)
    permissions = db.Column(db.Integer)
    users = relationship('User', backref='role', lazy='dynamic')

    @staticmethod
    async def insert_roles():
        roles = {
            'User': (Permission.COMMENT, True),
            'Administrator': (Permission.ADMINISTER, False)
        }
        for r, v in roles.items():
            role = await Role.query.where(Role.name == r).first()
            if not role:
                role = await Role.create(
                    name=r, permissions=v[0], default=v[1])
