import graphene

from user.mutations import Mutation
from user.query import Query

schema_user = graphene.Schema(query=Query, mutation=Mutation)
