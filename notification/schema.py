import graphene

from notification.mutations import Mutation
from notification.query import Query

schema_notification = graphene.Schema(query=Query, mutation=Mutation)
