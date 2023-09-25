import graphene
from notification.node import NotificationsInput, NotificationsReadInput, NotificationsType
from .models import Notifications
from datetime import datetime


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
        data = NotificationsInput(required=True)
    notifications = graphene.Field(NotificationsType)

    @staticmethod
    def mutate(root, info, data=None):
        Notifications.objects.update_or_create(pk=data.id, defaults=data)
        notification_instance = Notifications.objects.get(pk=data.id)
        return UpdateNotifications(notifications=notification_instance)


class NotificationRead(graphene.Mutation):
    class Arguments:
        data = NotificationsReadInput(required=True)
    message = graphene.String()

    @staticmethod
    def mutate(root, info, data=None):
        Notifications.objects.filter(id__in=data.get('ids'), last_read=None).update(is_read=True, last_read=datetime.now())
        return NotificationRead(message="All Notifications read")


class SendNotification(graphene.Mutation):
    class Arguments:
        notification_data = NotificationsInput(required=True)
    message = graphene.String()

    @staticmethod
    def mutate(root, info, notification_data=None):
        recipient_ids = notification_data.pop("recipient_ids")
        for recipient in recipient_ids:
            notification_instance = Notifications(**notification_data, recipient_id=recipient, created_date=datetime.now(), updated_date=datetime.now())
            notification_instance.save()
        return NotificationRead(message="Notification Send")


class Mutation(graphene.ObjectType):
    create_notification = CreateNotifications.Field()
    update_notification = UpdateNotifications.Field()
    is_notification_read = NotificationRead.Field()
    send_notification = SendNotification.Field()
