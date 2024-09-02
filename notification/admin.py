from django.contrib import admin
from .models import Notifications

# Register your models here.


class NotificationsAdmin(admin.ModelAdmin):
    list_display = ("id", "recipient", "message", "notification_type", "is_read")
    search_fields = ["id", "recipient"]
    list_filter = ("notification_type", "is_read")


admin.site.register(Notifications, NotificationsAdmin)
