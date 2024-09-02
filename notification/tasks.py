from datetime import datetime, timedelta
from notification.models import Notifications


def deleteNotifiations():
    """to delete all read notifications"""
    time_range = datetime.now() - timedelta(days=1)
    Notifications.objects.filter(last_read__lt=time_range).delete()
