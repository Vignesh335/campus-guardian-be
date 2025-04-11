import threading
import time
from django.apps import AppConfig
from django.utils.timezone import now
from datetime import timedelta


class ManagementConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'campus_guardian_main.management'

# attendance/apps.py


class AttendanceConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'campus_guardian_main.attendance'

    def ready(self):
        from django_cron import CronJobBase
        from campus_guardian_main.management.cron import DailyAttendanceAutoCreate

        def run_cron_daily():
            while True:
                current_time = now()
                target_time = current_time.replace(hour=2, minute=0, second=0, microsecond=0)
                if current_time > target_time:
                    target_time += timedelta(days=1)
                wait_seconds = (target_time - current_time).total_seconds()
                time.sleep(wait_seconds)

                try:
                    DailyAttendanceAutoCreate().do()
                    print("✅ DailyAttendanceAutoCreate ran successfully.")
                except Exception as e:
                    print(f"❌ Error running cron: {e}")

        if not hasattr(self, 'cron_thread_started'):
            self.cron_thread_started = True
            thread = threading.Thread(target=run_cron_daily, daemon=True)
            thread.start()
