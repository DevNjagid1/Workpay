from django.core.management.base import BaseCommand
from main.models import User

class Command(BaseCommand):
    help = 'Show all user credentials and roles'

    def handle(self, *args, **options):
        users = User.objects.all()
        self.stdout.write(self.style.SUCCESS('=== USER CREDENTIALS & ROLES ===\n'))
        
        for user in users:
            role = "ADMIN" if user.is_admin else "EMPLOYEE"
            self.stdout.write(f'Username: {user.username}')
            self.stdout.write(f'Role: {role}')
            self.stdout.write(f'Email: {user.email or "Not set"}')
            self.stdout.write(f'Admin: {user.is_admin}')
            self.stdout.write(f'Employee: {user.is_employee}')
            self.stdout.write(f'Superuser: {user.is_superuser}')
            self.stdout.write('---')
        
        self.stdout.write(self.style.SUCCESS(f'\nTotal Users: {users.count()}'))
