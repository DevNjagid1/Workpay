from django.core.management.base import BaseCommand
from main.email_utils import send_daily_attendance_summary

class Command(BaseCommand):
    help = 'Send daily attendance summary to admin'

    def handle(self, *args, **options):
        success = send_daily_attendance_summary()
        if success:
            self.stdout.write(self.style.SUCCESS('Daily attendance summary sent successfully!'))
        else:
            self.stdout.write(self.style.WARNING('No pending attendance to summarize.'))
