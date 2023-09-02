import graphene
# from graphene_file_upload.scalars import Upload
from graphene import relay
from graphene_django.filter import DjangoFilterConnectionField
from JobApplication.node import JobListType, JobListTypeAll


class Query(graphene.ObjectType):
    job_list = DjangoFilterConnectionField(JobListType)
    job_detail = relay.Node.Field(JobListTypeAll)
