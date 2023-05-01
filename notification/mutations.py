import graphene
from notification.node import NotificationsInput, NotificationsType
from .models import Notifications


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
