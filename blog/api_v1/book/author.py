from flask import url_for
from flask_restful import Resource
from flask_restful.reqparse import RequestParser

from blog.api_v1 import token_auth
from blog.api_v1.decorators import permission_required
from blog.models import Author, Permission


authors_parser = RequestParser()
authors_parser.add_argument('page', default=1)
authors_parser.add_argument('per_page', default=20)


class AuthorsResource(Resource):
    decorators = [
        permission_required(Permission.RESOURCE), token_auth.login_required
    ]

    def get(self):
        args = authors_parser.parse_args()
        authors_query = Author.query.filter_by().order_by(Author.name)

        pagination = authors_query.pagination(
            args.page, per_page=args.per_page, error_out=False)
        authors = pagination.items()

        if pagination.has_prev:
            prev = url_for(
                'book.authorsresource', page=args.page - 1, _external=True)
        if pagination.has_next:
            next_ = url_for(
                'book.authorsresource', page=args.page + 1, _external=True)
        
        return {
            'posts': [author.to_json() for author in authors],
            'prev_': prev,
            'next': next_,
            'count': pagination.total,
            'pages': pagination.pages,
        }
