from django.db import models


class User(models.Model):
    USER_TYPES = [
        ('ADMIN', 'Administrator'),
        ('DRIVER', 'Driver'),
        ('STUDENT', 'Student'),
        ('STAFF', 'Staff'),
    ]

    user_type = models.CharField(max_length=10, choices=USER_TYPES)
    phone = models.CharField(max_length=15)
    address = models.TextField(blank=True, null=True)
    email = models.CharField(max_length=100, blank=True, null=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    username = models.TextField(blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)

    def get_full_name(self):
        if self.last_name:
            return f"{self.first_name} {self.last_name}"
        return self.first_name

    def __str__(self):
        return f"{self.username} ({self.get_user_type_display()})"

    class Meta:
        db_table = 'users'
        # ordering = ['-check_in']