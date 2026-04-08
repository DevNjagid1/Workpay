from django.core.management.base import BaseCommand
import os

class Command(BaseCommand):
    help = 'Switch between console and SMTP email backends'

    def add_arguments(self, parser):
        parser.add_argument(
            'backend',
            type=str,
            choices=['console', 'smtp'],
            help='Email backend to switch to (console or smtp)'
        )

    def handle(self, *args, **options):
        backend = options['backend']
        settings_file = 'kazisafi/settings.py'
        
        try:
            with open(settings_file, 'r') as f:
                content = f.read()
            
            if backend == 'console':
                # Switch to console backend
                content = content.replace(
                    "EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'",
                    "EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'"
                )
                # Comment out SMTP settings
                lines = content.split('\n')
                new_lines = []
                for line in lines:
                    if line.strip().startswith('EMAIL_HOST =') or line.strip().startswith('EMAIL_PORT =') or line.strip().startswith('EMAIL_USE_TLS =') or line.strip().startswith('EMAIL_HOST_USER =') or line.strip().startswith('EMAIL_HOST_PASSWORD =') or line.strip().startswith('DEFAULT_FROM_EMAIL ='):
                        new_lines.append('# ' + line)
                    else:
                        new_lines.append(line)
                content = '\n'.join(new_lines)
                
            elif backend == 'smtp':
                # Switch to SMTP backend
                content = content.replace(
                    "EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'",
                    "EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'"
                )
                # Uncomment SMTP settings
                lines = content.split('\n')
                new_lines = []
                for line in lines:
                    if line.strip() == '# EMAIL_HOST = \'smtp.gmail.com\'':
                        new_lines.append('EMAIL_HOST = \'smtp.gmail.com\'')
                    elif line.strip() == '# EMAIL_PORT = 587':
                        new_lines.append('EMAIL_PORT = 587')
                    elif line.strip() == '# EMAIL_USE_TLS = True':
                        new_lines.append('EMAIL_USE_TLS = True')
                    elif line.strip() == '# EMAIL_HOST_USER = \'your-email@gmail.com\'':
                        new_lines.append('EMAIL_HOST_USER = \'your-email@gmail.com\'')
                    elif line.strip() == '# EMAIL_HOST_PASSWORD = \'your-16-character-app-password\'':
                        new_lines.append('EMAIL_HOST_PASSWORD = \'your-16-character-app-password\'')
                    elif line.strip() == '# DEFAULT_FROM_EMAIL = \'your-email@gmail.com\'':
                        new_lines.append('DEFAULT_FROM_EMAIL = \'your-email@gmail.com\'')
                    else:
                        new_lines.append(line)
                content = '\n'.join(new_lines)
            
            with open(settings_file, 'w') as f:
                f.write(content)
            
            self.stdout.write(self.style.SUCCESS(f'Switched to {backend} email backend'))
            
            if backend == 'smtp':
                self.stdout.write(self.style.WARNING('Remember to update your email credentials in settings.py!'))
                self.stdout.write(self.style.WARNING('See SMTP_SETUP_GUIDE.md for instructions'))
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error switching email backend: {str(e)}'))
