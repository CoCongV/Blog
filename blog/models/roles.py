# coding: utf-8
from blog import db
from blog.models.minixs import CRUDMixin, Serializer


class Permission:
    COMMENT = 0x02
    RESOURCE = 0X0A
    ADMINISTER = 0xff


class Role(db.Model, CRUDMixin, Serializer):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    default = db.Column(db.Boolean, default=False, index=True)
    permissions = db.Column(db.Integer)
    users = db.relationship('User', backref='role', lazy='dynamic')

    def __repr__(self):
        return str(self.json()).replace(',', '\n')

    @staticmethod
    def insert_roles():
        roles = {
            'User': [Permission.COMMENT],
            'Advanced_User': [Permission.COMMENT, Permission.RESOURCE],
            'Administrator': [Permission.ADMINISTER, Permission.COMMENT,
                              Permission.RESOURCE],
        }
        default_role = 'User'
        for r, p in roles.items():
            role = Role.query.filter_by(name=r).first()
            if role is None:
                role = Role(name=r)
            role.reset_permissions()
            for perm in p:
                role.add_permission(perm)
            role.default = (role.name == default_role)
            db.session.add(role)
        db.session.commit()

    def has_permission(self, perm):
        return self.permissions & perm == perm
    
    def add_permission(self, perm):
        if not self.has_permission(perm):
            self.permissions += perm
    
    def reset_permissions(self):
        self.permissions = 0
