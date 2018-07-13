from sqlalchemy.inspection import inspect

from blog import db


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
            try:
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                raise e
        return self

    def delete(self, commit=True):
        db.session.delete(self)
        return commit and db.session.commit()

    def update(self, commit=True, **kwargs):
        for attr, value in kwargs.items():
            setattr(self, attr, value)
        return commit and self.save() or self


class Serializer(object):
    serialized_fields = ()

    def json(self):
        serialized_fields = self.serialized_fields
        cls_serialized_fields = set(
            [column.name for column in self.__class__.__table__.columns])

        for primary_key in inspect(self.__class__).primary_key:
            if not getattr(self, primary_key.name):
                raise ValueError("The object hasn't been loaded yet.")

        if serialized_fields:
            for field in serialized_fields:
                if field not in cls_serialized_fields:
                    raise ValueError(
                        "The field `%r` isn't in `%r`"
                        % (field, self.__class__.__name__)
                    )
        else:
            serialized_fields = cls_serialized_fields
        ret = {}
        for field in serialized_fields:
            try:
                ret[field] = str(getattr(self, field))
            except UnicodeEncodeError as e:
                ret[field] = getattr(self, field)
        return ret
