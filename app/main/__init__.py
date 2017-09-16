# coding: utf-8
from flask import Blueprint
from flask_graphql import GraphQLView

from app.models.schema import schema

main = Blueprint('main', __name__)

main.add_url_rule('/graphql', view_func=GraphQLView.as_view('graphql', schema=schema, graphiql=True))

from . import views, errors
