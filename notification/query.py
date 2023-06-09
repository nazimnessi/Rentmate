import graphene
from graphene import relay
from graphene_django.filter import DjangoFilterConnectionField

from notification.node import NotificationsType


class Query(graphene.ObjectType):
    all_notifications = DjangoFilterConnectionField(NotificationsType)
    notifications = relay.Node.Field(NotificationsType)
