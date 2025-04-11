# models.py
from django.db import models
# from django.utils import timezone
import uuid
from datetime import date
from django.core.validators import MinLengthValidator

class Lecturer(models.Model):
    class LecturerType(models.TextChoices):
        FULL_TIME = 'FT', 'Full-Time'
        PART_TIME = 'PT', 'Part-Time'
        VISITING = 'VS', 'Visiting'
        ADJUNCT = 'AJ', 'Adjunct'

    display_name = models.CharField(max_length=100, validators=[MinLengthValidator(3)])
    type = models.CharField(max_length=2, choices=LecturerType.choices, default=LecturerType.FULL_TIME)
    department_name = models.CharField(max_length=100, validators=[MinLengthValidator(2)])
    is_active = models.BooleanField(default=True)
    staff_id = models.CharField(max_length=10, unique=True, editable=False)
    specialization = models.CharField(max_length=100, blank=True)
    joined_date = models.DateField()
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    webauthn_enabled = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.display_name} ({self.staff_id})"

    def save(self, *args, **kwargs):
        if not self.staff_id:
            dept_code = ''.join([c for c in self.department_name.upper() if c.isalpha()][:3])
            unique_part = uuid.uuid4().hex[:4].upper()
            self.staff_id = f"{dept_code}-{unique_part}"[:10]
        super().save(*args, **kwargs)


class Attendance(models.Model):
    class AttendanceStatus(models.TextChoices):
        PRESENT = 'PR', 'Present'
        ABSENT = 'AB', 'Absent'
        LATE = 'LT', 'Late'
        EXCUSED = 'EX', 'Excused'

    lecturer = models.ForeignKey('Lecturer', on_delete=models.CASCADE, related_name='attendances')
    date = models.DateField(default=date.today)
    status = models.CharField(max_length=2, choices=AttendanceStatus.choices, default=AttendanceStatus.PRESENT)
    remarks = models.TextField(blank=True)
    recorded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.lecturer.display_name} - {self.date} - {self.get_status_display()}"


# class WebAuthnCredential(models.Model):
#     lecturer = models.ForeignKey(Lecturer, on_delete=models.CASCADE, related_name='credentials')
#     credential_id = models.CharField(max_length=255, unique=True)
#     public_key = models.BinaryField()
#     sign_count = models.IntegerField(default=0)
#     credential_name = models.CharField(max_length=100, blank=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#
#     def __str__(self):
#         return f"Credential for {self.lecturer.display_name}"