import graphene
from graphene import relay
from graphene_django import DjangoObjectType
from .models import Notifications


class NotificationsType(DjangoObjectType):
    class Meta:
        model = Notifications
        filter_fields = {}
        interfaces = (relay.Node,)
        fields = "__all__"

    @classmethod
    def get_queryset(cls, queryset, info, **kwargs):
        user = info.context.user
        return queryset.filter(recipient_id=user.id).order_by("-id")


class NotificationsInput(graphene.InputObjectType):
    id = graphene.ID()
    recipient_id = graphene.Int()
    recipient_ids = graphene.List(graphene.Int)
    message = graphene.String()
    is_read = graphene.Boolean()
    notification_type = graphene.String()
    description = graphene.String()


class NotificationsReadInput(graphene.InputObjectType):
    ids = graphene.List(graphene.ID)
