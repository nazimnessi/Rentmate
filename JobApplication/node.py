import graphene
from graphene import relay
from graphene_django import DjangoObjectType
from .models import Job_Application, Job_List, Job_Types


class JobListTypeAll(DjangoObjectType):

    class Meta:
        model = Job_List
        interfaces = (relay.Node,)
        fields = "__all__"


class JobApplicationType(DjangoObjectType):

    class Meta:
        model = Job_Application
        interfaces = (relay.Node,)
        fields = "__all__"


class JobListType(DjangoObjectType):
    jobs = graphene.List(JobListTypeAll)

    def resolve_jobs(parent, info, **kwargs):

        return Job_List.objects.filter(jobTypes=parent.id)

    class Meta:
        model = Job_Types
        filter_fields = {}
        interfaces = (relay.Node,)
        fields = "__all__"


class JobApplicationInput(graphene.InputObjectType):
    id = graphene.ID()
    full_name = graphene.String()
    Job_List_id = graphene.Int()
    email = graphene.String()
    phone_number = graphene.String()
    linkedIn = graphene.String()
    github = graphene.String()
    website = graphene.String()
    total_experience = graphene.Int()
    questions = graphene.List(graphene.JSONString)
    resume = graphene.String()
    cover_letter = graphene.String()
    photo = graphene.String()
