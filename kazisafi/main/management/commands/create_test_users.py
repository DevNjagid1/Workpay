from django.core.management.base import BaseCommand
from main.models import User

class Command(BaseCommand):
    help = 'Create test users for development'

    def handle(self, *args, **options):
        # Create admin user
        if not User.objects.filter(username='admin').exists():
            admin = User.objects.create_user(
                username='admin',
                email='admin@kazisafi.com',
                password='Admin123456'
            )
            admin.is_admin = True
            admin.is_employee = False
            admin.is_superuser = True
            admin.save()
            self.stdout.write(self.style.SUCCESS('Created admin user: admin / Admin123456'))
        
        # Create test employee
        if not User.objects.filter(username='testemployee').exists():
            employee = User.objects.create_user(
                username='testemployee',
                email='test@kazisafi.com',
                password='Test123456'
            )
            employee.is_admin = False
            employee.is_employee = True
            employee.save()
            self.stdout.write(self.style.SUCCESS('Created test employee: testemployee / Test123456'))
        
        self.stdout.write(self.style.SUCCESS('Test users ready for development!'))
