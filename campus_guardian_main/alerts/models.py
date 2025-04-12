from django.db import models

class Alert(models.Model):
    ALERT_TYPES = [
        ('warning', 'Warning'),
        ('security', 'Security'),
        ('critical', 'Critical'),
        ('clear', 'Clear'),
    ]

    message = models.TextField()
    type = models.CharField(max_length=50, choices=ALERT_TYPES)
    timestamp = models.DateTimeField(auto_now_add=True)
    expiry = models.DateTimeField(blank=True, null=True)
    sender = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.type.upper()} - {self.message[:40]}"
