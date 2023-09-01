import graphene
# from user.mutations import Mutation
from JobApplication.query import Query


schema_job = graphene.Schema(query=Query, )
