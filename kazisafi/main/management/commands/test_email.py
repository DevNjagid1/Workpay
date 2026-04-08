from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.conf import settings

class Command(BaseCommand):
    help = 'Test email configuration'

    def handle(self, *args, **options):
        try:
            subject = 'Kazi Safi - Email Test'
            message = '''
            This is a test email from Kazi Safi Attendance Management System.
            
            If you receive this email, your email configuration is working correctly!
            
            System Details:
            - Backend: {backend}
            - From: {from_email}
            - To: {to_email}
            
            Sent at: {time}
            '''.format(
                backend=settings.EMAIL_BACKEND,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to_email=settings.NOTIFICATION_EMAIL,
                time=''.join(__import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
            )
            
            send_mail(
                subject=subject,
                message=message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.NOTIFICATION_EMAIL],
                fail_silently=False,
            )
            
            self.stdout.write(self.style.SUCCESS('Test email sent successfully!'))
            self.stdout.write(f'To: {settings.NOTIFICATION_EMAIL}')
            self.stdout.write(f'Backend: {settings.EMAIL_BACKEND}')
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Failed to send test email: {str(e)}'))
            self.stdout.write(self.style.WARNING('Check your email configuration in settings.py'))
