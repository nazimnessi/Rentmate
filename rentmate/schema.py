import graphene
from building import schema as schema_building
from graphene_django.debug import DjangoDebug
from notification import schema as schema_notification
from user import schema as schema_user
from JobApplication import schema as schema_job
from payment import schema as schema_payment
import graphql_jwt

from user.mutations import JWUserToken


class Query(
    schema_user.Query,
    schema_building.Query,
    schema_notification.Query,
    schema_job.Query,
    schema_payment.Query,
    graphene.ObjectType,
):
    debug = graphene.Field(DjangoDebug, name="_debug")


class Mutation(
    schema_user.Mutation,
    schema_building.Mutation,
    schema_notification.Mutation,
    schema_job.Mutation,
    schema_payment.Mutation,
    graphene.ObjectType,
):
    debug = graphene.Field(DjangoDebug, name="_debug")
    token_auth = JWUserToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
