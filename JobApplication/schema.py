import graphene
# from user.mutations import Mutation
from JobApplication.query import Query
from JobApplication.mutation import Mutation


schema_job = graphene.Schema(query=Query, mutation=Mutation)
