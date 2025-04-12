from django.db import models

class Bus(models.Model):
    LOCATION_STATUS_CHOICES = [
        ("in_campus", "In Campus"),
        ("out_campus", "Out of Campus"),
    ]
    SCHEDULE_STATUS_CHOICES = [
        ("scheduled", "Scheduled"),
        ("departed", "Departed"),
        ("arrived", "Arrived"),
    ]

    plate_number = models.CharField(max_length=20)
    model = models.CharField(max_length=50)
    capacity = models.IntegerField()
    status = models.CharField(max_length=20)
    location_status = models.CharField(max_length=20, choices=LOCATION_STATUS_CHOICES, default="in_campus")
    schedule_status = models.CharField(max_length=20, choices=SCHEDULE_STATUS_CHOICES, default="scheduled")

    def __str__(self):
        return self.plate_number

class Route(models.Model):
    name = models.CharField(max_length=100)
    start_point = models.CharField(max_length=100)
    end_point = models.CharField(max_length=100)
    stops = models.TextField()

    def __str__(self):
        return self.name

class Driver(models.Model):
    name = models.CharField(max_length=100)
    license_no = models.CharField(max_length=50)
    assigned_bus = models.ForeignKey(Bus, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name

class Schedule(models.Model):
    route = models.ForeignKey(Route, on_delete=models.CASCADE)
    bus = models.ForeignKey(Bus, on_delete=models.CASCADE)
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()

    def __str__(self):
        return f"{self.bus} on {self.route} ({self.departure_time} - {self.arrival_time})"


from django.db import models
from django.utils import timezone


class StopTime(models.Model):
    STATUS_CHOICES = [
        ('upcoming', 'Upcoming'),
        ('arrived', 'Arrived'),
        ('skipped', 'Skipped'),
    ]

    schedule = models.ForeignKey(
        'Schedule',
        related_name='stop_times',
        on_delete=models.CASCADE,
        verbose_name="Related Schedule"
    )
    stop_name = models.CharField(max_length=100)
    arrival_time = models.DateTimeField(help_text="Scheduled arrival time")

    actual_arrival_time = models.DateTimeField(
        null=True, blank=True,
        help_text="When the bus actually reached the stop"
    )
    stop_status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='upcoming',
        help_text="Status of the stop (e.g. upcoming, arrived, skipped)"
    )

    class Meta:
        ordering = ['arrival_time']
        indexes = [
            models.Index(fields=['arrival_time']),
        ]

    def __str__(self):
        return f"{self.stop_name} at {self.arrival_time.strftime('%Y-%m-%d %H:%M')}"

    def late_by_minutes(self):
        """Returns delay in minutes (positive if late, negative if early)."""
        if self.actual_arrival_time:
            diff = self.actual_arrival_time - self.arrival_time
            return int(diff.total_seconds() // 60)
        return None

    def update_status(self):
        """Auto-update stop_status based on time and actual arrival."""
        now = timezone.now()
        if self.actual_arrival_time:
            self.stop_status = "arrived"
        elif self.arrival_time < now:
            self.stop_status = "skipped"
        else:
            self.stop_status = "upcoming"
        self.save()


class GPSLog(models.Model):
    ENTRY = 'entry'
    EXIT = 'exit'

    LOG_TYPES = [
        (ENTRY, 'Entry'),
        (EXIT, 'Exit'),
    ]

    bus = models.ForeignKey(Bus, on_delete=models.CASCADE)
    latitude = models.FloatField(null=False, blank=False)
    longitude = models.FloatField(null=False, blank=False)
    timestamp = models.DateTimeField(auto_now_add=True, null=False, blank=False)
    log_type = models.CharField(max_length=5, choices=LOG_TYPES, default=ENTRY)  # Entry or Exit log

    def __str__(self):
        return f"GPS Log for Bus {self.bus.id} - {self.get_log_type_display()} at {self.timestamp}"