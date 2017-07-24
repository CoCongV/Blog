import graphene
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyConnectionField, SQLAlchemyObjectType
from .posts import Post as PostModel


class PostQuery(SQLAlchemyObjectType):
    
    class Meta:
        model = PostModel
        interfaces = (relay.Node, )


class Query(graphene.ObjectType):
    node = relay.Node.Field()
    posts = SQLAlchemyConnectionField(PostQuery)

schema = graphene.Schema(query=Query, types=[PostQuery])
