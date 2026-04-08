from django.core.management.base import BaseCommand
from main.models import Attendance, Earning

class Command(BaseCommand):
    help = 'Clear all attendance and earning data for testing'

    def handle(self, *args, **options):
        # Clear all attendance records
        attendance_count = Attendance.objects.count()
        Attendance.objects.all().delete()
        self.stdout.write(self.style.SUCCESS(f'Deleted {attendance_count} attendance records'))
        
        # Clear all earning records
        earning_count = Earning.objects.count()
        Earning.objects.all().delete()
        self.stdout.write(self.style.SUCCESS(f'Deleted {earning_count} earning records'))
        
        self.stdout.write(self.style.SUCCESS('All attendance data cleared for fresh testing'))
