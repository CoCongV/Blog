from flask import url_for, current_app
from flask_restful import Resource
from flask_restful.reqparse import RequestParser
from werkzeug.datastructures import FileStorage

from blog import db
from blog.api_v1 import token_auth
from blog.models import Book


books_parser = RequestParser()
books_parser.add_argument('page', type=int, default=1)

books_post_parser = RequestParser()
books_post_parser.add_argument('book', type=FileStorage, required=True)
books_post_parser.add_argument('name', required=True)
books_post_parser.add_argument('cover_img', type=FileStorage)

class BooksResource(Resource):

    decorators = [token_auth.login_required, ]
    
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
        
        