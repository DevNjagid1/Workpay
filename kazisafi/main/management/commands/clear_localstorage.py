from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Clear localStorage data for testing'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('=== LOCALSTORAGE CLEAR INSTRUCTIONS ===\n'))
        self.stdout.write('To clear localStorage in browser:')
        self.stdout.write('1. Open browser developer tools (F12)')
        self.stdout.write('2. Go to Console tab')
        self.stdout.write('3. Type: localStorage.clear()')
        self.stdout.write('4. Press Enter')
        self.stdout.write('5. Refresh the page')
        self.stdout.write(self.style.SUCCESS('\nThis will clear all cached data!'))
