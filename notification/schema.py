import graphene
from graphene import relay
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from .models import Notifications


class NotificationsType(DjangoObjectType):
    class Meta:
        model = Notifications
        filter_fields = {}
        interfaces = (relay.Node,)
        fields = '__all__'


class Query(graphene.ObjectType):
    all_Notifications = DjangoFilterConnectionField(NotificationsType)
    notifications = relay.Node.Field(NotificationsType)

    def resolve_all_Notifications(root, info, **kwargs):
        return Notifications.objects.order_by('-id')


class NotificationsInput(graphene.InputObjectType):
    id = graphene.ID()
    recipient_id = graphene.Int()
    message = graphene.String()
    is_read = graphene.Boolean()
    notification_type = graphene.String()
    description = graphene.String()


class CreateNotifications(graphene.Mutation):
    class Arguments:
        notification_data = NotificationsInput(required=True)
    notifications = graphene.Field(NotificationsType)

    @staticmethod
    def mutate(root, info, notification_data=None):
        try:
            notification_instance = Notifications(**notification_data)
            notification_instance.save()
        except Exception:
            notification_instance = None
        return CreateNotifications(notifications=notification_instance)


class UpdateNotifications(graphene.Mutation):
    class Arguments:
        notification_data = NotificationsInput(required=True)
    notifications = graphene.Field(NotificationsType)

    @staticmethod
    def mutate(root, info, notification_data=None):
        Notifications.objects.update_or_create(pk=notification_data.id, defaults=notification_data)
        notification_instance = Notifications.objects.get(pk=notification_data.id)
        return UpdateNotifications(notifications=notification_instance)


class Mutation(graphene.ObjectType):
    create_notification = CreateNotifications.Field()
    update_notification = UpdateNotifications.Field()


schema_building = graphene.Schema(query=Query, mutation=Mutation)
