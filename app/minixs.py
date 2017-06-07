from sqlalchemy.inspection import inspect

from . import db

class CRUDMixin(object):
    """Implements methods to create, read, update, and delete"""

    @classmethod
    def create(cls, commit=True, **kwargs):
        instance = cls(**kwargs)
        return instance.save(commit)

    @classmethod
    def get(cls, id):
        return cls.query.get(id)

    @classmethod
    def get_or_404(cls, id):
        return cls.query.get_or_404(id)

    @classmethod
    def get_or_create(cls, id, commit=True, **kwargs):
        obj = cls.query.get(id) or cls(id)
        obj.update(commit=False, **kwargs)
        return obj.save(commit=commit)

    @classmethod
    def _filter(cls, **kwargs):
        query = cls.query
        for key, value in kwargs.items():
            query = query.filer_by(**{key: value})
        return query.first()

    @classmethod
    def filter_or_create(cls, commit=True, **kwargs):
        self = cls._filter(**kwargs)
        if not self:
            self = cls.create(commit, **kwargs)
        return self

    def save(self, commit=True):
        db.session.add(self)
        if commit:
            db.session.commit()
        return self

    def delete(self, commit=True):
        db.session.delete(self)
        return commit and db.session.commit()

    def update(self, commit=True, **kwargs):
        for attr, value in kwargs.items():
            setattr(self, attr, value)
        return commit and self.save() or self