import graphene
from building.mutations import Mutation
from building.query import Query


schema_building = graphene.Schema(query=Query, mutation=Mutation)
