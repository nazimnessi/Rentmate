import graphene
from graphene import relay
from graphene_django.filter import DjangoFilterConnectionField

from notification.node import NotificationsType
from .models import Notifications


class Query(graphene.ObjectType):
    all_Notifications = DjangoFilterConnectionField(NotificationsType)
    notifications = relay.Node.Field(NotificationsType)

    def resolve_all_Notifications(root, info, **kwargs):
        return Notifications.objects.order_by('-id')
