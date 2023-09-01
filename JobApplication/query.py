import graphene
# from graphene_file_upload.scalars import Upload
from graphene_django.filter import DjangoFilterConnectionField
from JobApplication.node import JobListType


class Query(graphene.ObjectType):
    job_list = DjangoFilterConnectionField(JobListType)
