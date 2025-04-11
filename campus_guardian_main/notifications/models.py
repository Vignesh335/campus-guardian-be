# notifications/models.py

from django.db import models
from django.utils import timezone


class Notification(models.Model):
    # Correct model references using the 'app_label.ModelName' format
    management = models.ForeignKey('management.Lecturer', on_delete=models.CASCADE)
    visitor = models.ForeignKey('visitors.Visitor', on_delete=models.CASCADE)

    title = models.CharField(max_length=255)
    message = models.TextField()
    # email = models.EmailField()
    notification_time = models.DateTimeField(default=timezone.now)
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.title} - {self.management.name} - {self.visitor.name}"
