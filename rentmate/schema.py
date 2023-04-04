import graphene
from building import schema as schema_building
from graphene_django.debug import DjangoDebug
from user import schema as schema_user


class Query(
    schema_user.Query,
    schema_building.Query,
    graphene.ObjectType,
):
    debug = graphene.Field(DjangoDebug, name="_debug")


class Mutation(
    schema_user.Mutation,
    schema_building.Mutation,
    graphene.ObjectType,
):
    debug = graphene.Field(DjangoDebug, name="_debug")


schema = graphene.Schema(query=Query, mutation=Mutation)
