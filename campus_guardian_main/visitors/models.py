from django.db import models
from django.utils import timezone


class Visitor(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('APPROVED', 'Approved'),
        ('DENIED', 'Denied'),
    ]

    VISITOR_TYPES = [
        ('STD', 'Student'),
        ('PAR', 'Parent'),
        ('VND', 'Vendor'),
        ('GST', 'Guest'),
    ]

    name = models.CharField(max_length=100)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=15, null=True)
    visitor_type = models.CharField(max_length=3, choices=VISITOR_TYPES, default="GST")
    whom_to_meet = models.CharField(max_length=100, blank=True, null=True)
    purpose = models.TextField()
    photo = models.ImageField(upload_to='visitor_photos/')
    id_proof = models.FileField(upload_to='visitor_ids/', null=True, blank=True)
    check_in = models.DateTimeField(default=timezone.now)
    check_out = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')
    denial_reason = models.TextField(blank=True, null=True)

    # def __str__(self):
    #     return f"{self.name} ({self.get_status_display()})"

    class Meta:
        db_table = 'visitors'
        ordering = ['-check_in']