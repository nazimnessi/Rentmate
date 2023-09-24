import graphene
from graphene import relay
from graphql import GraphQLError
# from graphene_file_upload.scalars import Upload
from graphene_django.filter import DjangoFilterConnectionField

from user.node import AddressType, RenterType, UserType
from .models import User, Address


class Query(graphene.ObjectType):
    all_users = DjangoFilterConnectionField(UserType)
    users = relay.Node.Field(UserType)
    logged_in_user = graphene.Field(UserType)
    all_Renters = DjangoFilterConnectionField(RenterType)

    all_address = DjangoFilterConnectionField(AddressType)
    address = relay.Node.Field(AddressType)

    def resolve_all_users(root, info, **kwargs):
        return User.objects.order_by('-id')

    def resolve_logged_in_user(root, info, **kwargs):
        user = info.context.user
        if not user.is_authenticated:
            raise GraphQLError("Authentication credentials were not provided")
        return user

    def resolve_all_address(root, info, **kwargs):
        return Address.objects.order_by('-id')

    def resolve_all_Renters(root, info, **kwargs):
        return User.objects.filter(renter__building__owner=info.context.user).distinct()
