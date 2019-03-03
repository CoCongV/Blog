from datetime import datetime
import os
from pathlib import Path

from flask import url_for, current_app, g, send_from_directory
from flask_restful import Resource
from flask_restful.reqparse import RequestParser
from werkzeug.datastructures import FileStorage

from blog import db, books
from blog.api_v1 import token_auth
from blog.api_v1.decorators import permission_required
from blog.exceptions import AlreadyExists
from blog.models import Book, Permission, Category, Author


books_parser = RequestParser()
books_parser.add_argument('page', type=int, default=1)
books_parser.add_argument('num', type=int, default=15)

books_post_parser = RequestParser()
books_post_parser.add_argument(
    'book', type=FileStorage, required=True, location='files')
books_post_parser.add_argument('name', location='form')
books_post_parser.add_argument('cover_img', type=FileStorage, location='files')
books_post_parser.add_argument('author_ids', action='append')
books_post_parser.add_argument('category_ids', action='append')


class BooksResource(Resource):

    decorators = [
        permission_required(Permission.RESOURCE),
        token_auth.login_required,
    ]

    def get(self):
        args = books_parser.parse_args()
        prev = None
        next_ = None
        per_page = args.num or current_app.config.get('BLOG_BOOK_PER_PAGE', 15)
        book_query = Book.query.filter_by().order_by(
            db.desc('upload_time'))

        pagination = book_query.paginate(
            args.page, per_page, error_out=False)
        books = pagination.items

        if pagination.has_prev:
            prev = url_for(
                'book.booksresource', page=args.page - 1, _external=True)
        if pagination.has_next:
            next_ = url_for(
                'book.booksresource', page=args.page + 1, _external=True)

        return {
            'books': [book.json() for book in books],
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
        book.authors.append(
            Author.query.filter(Author.id.in_(args.author_ids)))
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
        permission_required(Permission.RESOURCE),
        token_auth.login_required,
    ]

    def get(self, book_id):
        book = Book.get_or_404(book_id)
        return send_from_directory(current_app.config['UPLOADED_BOOKS_DEST'],
                                   book.file)

    @permission_required(Permission.ADMINISTER)
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

    @permission_required(Permission.ADMINISTER)
    def delete(self, book_id):
        book = Book.get_or_404(book_id)
        path = Path(os.path.join(books.config.destination, book.file))
        path.unlink()
        book.delete()
        return ''


search_parse = RequestParser()
search_parse.add_argument('param', location='args')
search_parse.add_argument('page', location='args', type=int, default=1)

class BookSearch(Resource):
    def get(self):
        prev = None
        next_ = None
        total = 0
        per_page = current_app.config['BLOG_BOOK_PER_PAGE']

        args = search_parse.parse_args()
        book_query = Book.query.filter_by()
        if args.param:
            pagination = book_query.whoosh_search(args.param).paginate(
                args.page, per_page=per_page, error_out=False)
        else:
            pagination = None
        if pagination:
            books = pagination.items
            total = pagination.total
            if pagination.has_prev:
                prev = url_for(
                    'post.post_search', page=args.page - 1, _external=True)
            if pagination.has_next:
                next_ = url_for(
                    'post.post_search', page=args.page + 1, _external=True)
        else:
            books = []
        return {'books': [i.json() for i in books],
                'prev': prev,
                'next': next_,
                'count': total}
