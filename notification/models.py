from django.db import models
from user.models import User
# Create your models here.


class Notifications(models.Model):
    NOTIFICATION_TYPES = (
        ('payment', 'Payment'),
        ('maintenance', 'Maintenance'),
        ('application', 'Application'),
        ('others', 'Others'),
    )
    recipient = models.ForeignKey(User, on_delete=models.CASCADE)
    created_date = models.DateTimeField('Notifications created date', auto_now_add=True)
    updated_date = models.DateTimeField('Notifications updated date', auto_now_add=True)
    message = models.CharField(max_length=255, blank=True, null=True)
    is_read = models.BooleanField(default=False)
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES, default='others')
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return str(self.recipient)
