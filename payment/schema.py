import graphene
from payment.mutations import Mutation
from payment.query import Query


schema_user = graphene.Schema(query=Query, mutation=Mutation)
