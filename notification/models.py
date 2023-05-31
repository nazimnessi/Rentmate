from django.db import models
from user.models import User
# Create your models here.


class Notifications(models.Model):
    NOTIFICATION_TYPES = (
        ('Payment', 'Payment'),
        ('Maintenance', 'Maintenance'),
        ('Application', 'Application'),
        ('Others', 'Others'),
    )
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name="recipient")
    sender = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name="sender")
    created_date = models.DateTimeField('Notifications created date', auto_now_add=True)
    updated_date = models.DateTimeField('Notifications updated date', auto_now_add=True)
    message = models.CharField(max_length=255, blank=True, null=True)
    is_read = models.BooleanField(default=False)
    last_read = models.DateField("Notifications read date", blank=True, null=True)
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES, default='Others')
    description = models.TextField(blank=True, null=True)
    request = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return str(self.recipient)
