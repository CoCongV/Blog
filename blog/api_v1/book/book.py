from datetime import datetime
import os
from pathlib import Path

from flask import url_for, current_app, g, send_from_directory
from flask_restful import Resource
from flask_restful.reqparse import RequestParser
from werkzeug.datastructures import FileStorage

from blog import db, books
from blog.api_v1 import token_auth
from blog.decorators import permission_required
from blog.exceptions import AlreadyExists
from blog.models import Book, Permission, Category, Author


books_parser = RequestParser()
books_parser.add_argument('page', type=int, default=1)

books_post_parser = RequestParser()
books_post_parser.add_argument(
    'book', type=FileStorage, required=True, location='files')
books_post_parser.add_argument('name', location='form')
books_post_parser.add_argument('cover_img', type=FileStorage, location='files')
books_post_parser.add_argument('author_ids', action='append')
books_post_parser.add_argument('category_ids', action='append')


class BooksResource(Resource):

    decorators = [
        token_auth.login_required,
        permission_required(Permission.RESOURCE)
    ]

    def get(self):
        args = books_parser.parse_args()
        prev = None
        next_ = None
        per_page = current_app.config.get('BOOK_PER_PAGE', 20)
        book_query = Book.query.filter_by().order_by(
            db.desc('upload_time'))

        pagination = book_query.pagination(
            args.page, per_page, error_out=False)
        books = pagination.items

        if pagination.has_prev:
            prev = url_for(
                'book.booksresource', page=args.page - 1, _external=True)
        if pagination.has_next:
            next_ = url_for(
                'book.booksresource', page=args.page + 1, _external=True)

        return {
            'books': [book.to_json() for book in books],
            'prev': prev,
            'next': next_,
            'count': pagination.total,
            'pages': pagination.pages,
        }

    def post(self):
        args = books_post_parser.parse_args()
        name = f"{args.name}_{g.current_app.id}_{datetime.now().strftime('%Y-%m-%d')}.{args.book.filename.split('.')[-1]}"
        filename = books.save(args.book, name=name)

        book = Book(name=args.name, file=filename)
        book.categories = Category.query.filter(
            Category.id.in_(args.category_ids))
        book.authors = Author.query.filter(Author.id.in_(args.author_ids))
        book.save()
        file_url = books.url(filename)
        return {'url': file_url}


book_parser = RequestParser()
book_parser.add_argument('name')
book_parser.add_argument('author_ids', action='append')
book_parser.add_argument('category_ids', action='append')
books_post_parser.add_argument('book', type=FileStorage, location='files')


class BookResource(Resource):
    decorators = [
        token_auth.login_required,
        permission_required(Permission.RESOURCE)
    ]

    method_decorators = {
        'patch': permission_required(Permission.ADMINISTER),
        'delete': permission_required(Permission.ADMINISTER)
    }

    def get(self, book_id):
        book = Book.get_or_404(book_id)
        return send_from_directory(current_app.config['UPLOADED_BOOK_DEST'],
                                   book.file)

    def patch(self, book_id):
        args = book_parser.parse_args()
        book = Book.get_or_404(book_id)
        if args.name:
            book.name = args.name
        if args.author_ids:
            book.authors = Author.query.filter(Author.id.in_(args.author_ids))
        if args.category_ids:
            book.categories = Category.query.filter(
                Category.id.in_(args.category_ids))
        if args.book:
            path = Path(os.path.join(books.config.destination, book.file))
            path.unlink()
            name = f"{book.name}_{g.current_app.id}_{datetime.now().strftime('%Y-%m-%d')}.{args.book.filename.split('.')[-1]}"
            filename = books.save(args.book, name=name)
            book.update(file=filename)
        return ''

    def delete(self, book_id):
        book = Book.get_or_404(book_id)
        path = Path(os.path.join(books.config.destination, book.file))
        path.unlink()
        book.delete()
        return ''
