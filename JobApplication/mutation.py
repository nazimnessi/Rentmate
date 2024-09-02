import graphene
from graphql import GraphQLError
from JobApplication.models import Job_Application
from JobApplication.node import JobApplicationInput, JobApplicationType
from django.db import transaction


class CreateJobApplication(graphene.Mutation):
    class Arguments:
        jobApplications = JobApplicationInput(required=True)

    jobApplications = graphene.Field(JobApplicationType)

    @staticmethod
    def mutate(root, info, jobApplications=None):
        try:
            with transaction.atomic():
                application_instance = Job_Application.objects.create(**jobApplications)
        except Exception as exe:
            transaction.rollback()
            raise GraphQLError(
                f"unknown error occurred in job application creation error: {exe}"
            )
        return CreateJobApplication(jobApplications=application_instance)


class Mutation(graphene.ObjectType):
    create_job_application = CreateJobApplication.Field()
