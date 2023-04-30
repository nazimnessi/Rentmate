import graphene
from graphene import relay
from graphene_django import DjangoObjectType
from .models import Notifications


class NotificationsType(DjangoObjectType):
    class Meta:
        model = Notifications
        filter_fields = {}
        interfaces = (relay.Node,)
        fields = '__all__'


class NotificationsInput(graphene.InputObjectType):
    id = graphene.ID()
    recipient_id = graphene.Int()
    message = graphene.String()
    is_read = graphene.Boolean()
    notification_type = graphene.String()
    description = graphene.String()
