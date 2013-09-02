from django.db import models

from sentry.models import Group


class NotificationEvent(models.Model):
    group = models.ForeignKey(Group)
    notified_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        get_latest_by = 'notified_at'
