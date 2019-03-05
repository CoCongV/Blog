from datetime import datetime
import os
from pathlib import Path

from flask import current_app
from sqlalchemy import Table, Column, Integer, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from whoosh.analysis import SimpleAnalyzer

from blog import db
from blog.models.minixs import CRUDMixin, Serializer

Base = declarative_base()


# author_book = Table('author_book', Base.metadata,
#     Column('author_id', Integer, ForeignKey('author.id')),
#     Column('book_id', Integer, ForeignKey('book.id')))

class AuthorBook(db.Model):
    __tablename__ = 'author_book'
    author_id = db.Column(
        db.Integer, db.ForeignKey('author.id'), primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), primary_key=True)



class Author(db.Model, CRUDMixin, Serializer):
    __tablename__ = 'author'
    __searchable__ = ['name']
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), index=True, nullable=False)
    country = db.Column(db.String(32), index=True)
    remark = db.Column(db.String(32))

    books = db.relationship(
        'Book', secondary='author_book', back_populates='authors')


# category_book = Table('category_book', Base.metadata,
#     Column('category_id', Integer, ForeignKey('category.id')),
#     Column('book_id', Integer, ForeignKey('book.id')))
class CategoryBook(db.Model):
    __tablename__ = 'category_book'
    category_id = db.Column(
        db.Integer, db.ForeignKey('category.id'), primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), primary_key=True)



class Category(db.Model, CRUDMixin, Serializer):
    __tablename__ = 'category'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Integer, index=True, nullable=False)
    books = db.relationship(
        'Book', secondary='category_book', back_populates='categories')


class Book(db.Model, CRUDMixin, Serializer):
    __tablename__ = 'book'
    __searchable__ = ['name']
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, index=True)
    file = db.Column(db.String(64), nullable=False, unique=True)
    cover_img = db.Column(db.Text)
    upload_time = db.Column(db.DateTime, default=lambda: datetime.utcnow())

    creator_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    creator = db.relationship(
        'User', back_populates='books')
    authors = db.relationship(
        'Author', secondary='author_book', back_populates='books')
    categories = db.relationship(
        'Category', secondary='category_book', back_populates='books')

    def read(self):
        with open(self.path, 'rb') as f:
            yield f.readline()

    def json(self):
        r = super().json()
        r['authors'] = [i.name for i in self.authors]
        r['creator'] = self.creator.username
        return r

    def delete(self, commit=True):
        path = Path(
            os.path.join(current_app.config['UPLOADED_BOOKS_DEST'], self.file))
        path.unlink()
        return super().delete(commit)
