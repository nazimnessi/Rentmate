import graphene
import graphql_jwt
from graphene_django.debug import DjangoDebug

from building import schema as schema_building
from notification import schema as schema_notification
from user import schema as schema_user
from user.mutations import JWUserToken


class Query(
    schema_user.Query,
    schema_building.Query,
    schema_notification.Query,
    graphene.ObjectType,
):
    debug = graphene.Field(DjangoDebug, name="_debug")


class Mutation(
    schema_user.Mutation,
    schema_building.Mutation,
    schema_notification.Mutation,
    graphene.ObjectType,
):
    debug = graphene.Field(DjangoDebug, name="_debug")
    token_auth = JWUserToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
