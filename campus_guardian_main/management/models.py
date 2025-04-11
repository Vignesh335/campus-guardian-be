from django.db import models
import uuid
from django.core.validators import MinLengthValidator

class Lecturer(models.Model):
    class LecturerType(models.TextChoices):
        FULL_TIME = 'FT', 'Full-Time'
        PART_TIME = 'PT', 'Part-Time'
        VISITING = 'VS', 'Visiting'
        ADJUNCT = 'AJ', 'Adjunct'

    display_name = models.CharField(
        max_length=100,
        validators=[MinLengthValidator(3)]
    )
    type = models.CharField(
        max_length=2,
        choices=LecturerType.choices,
        default=LecturerType.FULL_TIME
    )
    department_name = models.CharField(
        max_length=100,
        validators=[MinLengthValidator(2)]
    )
    is_active = models.BooleanField(default=True)
    staff_id = models.CharField(
        max_length=10,  # Reduced to ensure safety
        unique=True,
        editable=False
    )
    specialization = models.CharField(max_length=100, blank=True)
    joined_date = models.DateField()
    email = models.CharField(max_length=100, default="default@email.com")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.display_name} ({self.staff_id})"

    def save(self, *args, **kwargs):
        if not self.staff_id:
            # Generate compact ID: DEPT-XXXX
            dept_code = ''.join([c for c in self.department_name.upper() if c.isalpha()][:3])
            unique_part = uuid.uuid4().hex[:4].upper()
            self.staff_id = f"{dept_code}-{unique_part}"[:10]  # Ensures max_length=10
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['-joined_date']
        db_table = 'management'
        verbose_name = 'Lecturer'
        verbose_name_plural = 'Lecturers'