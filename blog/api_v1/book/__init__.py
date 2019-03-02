from flask import Blueprint
from flask_restful import Api

api_book = Blueprint('book', __name__, url_prefix='/books')
api = Api(api_book)

from .author import AuthorsResource
from .book import BooksResource, BookResource

api.add_resource(BooksResource, '/')
api.add_resource(BookResource,'/<int:book_id>/')
