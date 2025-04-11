from django.db import models
from django.utils import timezone

from campus_guardian_main.users.models import User


class Bus(models.Model):
    BUS_TYPES = [
        ('REG', 'Regular'),
        ('EXP', 'Express'),
        ('VIP', 'VIP'),
    ]

    bus_number = models.CharField(max_length=20, unique=True)
    bus_type = models.CharField(max_length=3, choices=BUS_TYPES, default='REG')
    capacity = models.PositiveIntegerField()
    license_plate = models.CharField(max_length=15, unique=True)
    latitude = models.FloatField(blank=True, null=True)   # ✅ replaced PointField
    longitude = models.FloatField(blank=True, null=True)  # ✅ replaced PointField
    is_active = models.BooleanField(default=True)
    added_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.bus_number} ({self.get_bus_type_display()})"


class Driver(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    license_number = models.CharField(max_length=20, unique=True)
    years_of_experience = models.PositiveIntegerField(default=0)
    assigned_bus = models.OneToOneField(Bus, on_delete=models.SET_NULL, null=True, blank=True, related_name='driver')

    def __str__(self):
        return f"{self.user.get_full_name()} (License: {self.license_number})"


class Route(models.Model):
    name = models.CharField(max_length=100)
    origin = models.CharField(max_length=100)
    destination = models.CharField(max_length=100)
    stops = models.JSONField()
    distance = models.FloatField()
    estimated_duration = models.DurationField()

    def __str__(self):
        return f"{self.name} ({self.origin} to {self.destination})"


class BusSchedule(models.Model):
    bus = models.ForeignKey(Bus, on_delete=models.CASCADE, related_name='schedules')
    route = models.ForeignKey(Route, on_delete=models.CASCADE, related_name='schedules')
    departure_time = models.TimeField()
    arrival_time = models.TimeField()
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['departure_time']

    def __str__(self):
        return f"{self.bus} on {self.route} at {self.departure_time}"


class BusLocationHistory(models.Model):
    STATUS_CHOICES = [
        ('on_campus', 'On Campus'),
        ('scheduled', 'Scheduled'),
        ('departed', 'Departed'),
    ]

    bus = models.ForeignKey(Bus, on_delete=models.CASCADE, related_name='location_history')
    latitude = models.FloatField()
    longitude = models.FloatField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='On Campus')
    timestamp = models.DateTimeField(default=timezone.now)
    speed = models.FloatField(blank=True, null=True)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.bus} at {self.timestamp}"
