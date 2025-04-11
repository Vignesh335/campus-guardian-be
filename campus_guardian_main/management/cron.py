from django_cron import CronJobBase, Schedule
from .models import Lecturer, Attendance
from datetime import date
from django.utils.timezone import now

class DailyAttendanceAutoCreate(CronJobBase):
    RUN_EVERY_MINS = 60 * 24  # once a day

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'attendance.daily_auto_attendance'

    def do(self):
        today = date.today()
        lecturers = Lecturer.objects.filter(is_active=True)

        created_count = 0

        for lecturer in lecturers:
            attendance, created = Attendance.objects.get_or_create(
                lecturer=lecturer,
                date=today,
                defaults={
                    'status': Attendance.AttendanceStatus.ABSENT,
                    'remarks': 'Auto-marked as absent',
                }
            )
            if created:
                created_count += 1

        print(f"[Cron] Created {created_count} auto-attendance records for {today}")
