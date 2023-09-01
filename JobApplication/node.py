import graphene
from graphene import relay
from graphene_django import DjangoObjectType
from .models import Job_List, Job_Types


class JobListTypeAll(DjangoObjectType):

    class Meta:
        model = Job_List
        interfaces = (relay.Node,)
        fields = '__all__'


class JobListType(DjangoObjectType):
    jobs = graphene.List(JobListTypeAll)

    def resolve_jobs(parent, info, **kwargs):

        return Job_List.objects.filter(jobTypes=parent.id)

    class Meta:
        model = Job_Types
        filter_fields = {}
        interfaces = (relay.Node,)
        fields = '__all__'
