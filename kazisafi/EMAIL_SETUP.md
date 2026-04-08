# Email Configuration Guide

## Development (Current Setup)
Currently configured to use **Console Backend** - emails are printed to terminal:

```python
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
```

## Production Setup

### 1. Gmail SMTP Setup
Update `settings.py` with your Gmail credentials:

```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@gmail.com'
EMAIL_HOST_PASSWORD = 'your-app-password'  # Use App Password, not regular password
DEFAULT_FROM_EMAIL = 'your-email@gmail.com'
NOTIFICATION_EMAIL = 'admin@yourcompany.com'
```

### 2. Gmail App Password
1. Enable 2-factor authentication on your Gmail account
2. Go to Google Account settings > Security > App passwords
3. Generate a new app password for "Kazi Safi"
4. Use this app password in `EMAIL_HOST_PASSWORD`

### 3. Other Email Providers

#### Outlook/Hotmail
```python
EMAIL_HOST = 'smtp-mail.outlook.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
```

#### SendGrid
```python
EMAIL_HOST = 'smtp.sendgrid.net'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'apikey'
EMAIL_HOST_PASSWORD = 'your-sendgrid-api-key'
```

## Email Types

### 1. Admin Notifications
- **Trigger**: Employee marks attendance
- **Recipient**: Admin email
- **Content**: Employee info, attendance details, approval link

### 2. Employee Notifications
- **Approval**: When admin approves attendance
- **Rejection**: When admin rejects attendance (with reason)
- **Recipient**: Employee email

### 3. Daily Summary
- **Trigger**: Can be scheduled daily
- **Content**: Summary of all pending attendance
- **Command**: `python manage.py send_daily_summary`

## Testing

### Test Email Configuration
```bash
python manage.py test_email
```

### Test Attendance Notification
```bash
python manage.py shell
```
```python
from main.email_utils import send_attendance_notification
from main.models import Attendance
attendance = Attendance.objects.first()
send_attendance_notification(attendance)
```

## Automation

### Schedule Daily Summary (Linux Cron)
```bash
# Run daily at 9 AM
0 9 * * * /path/to/venv/bin/python /path/to/project/manage.py send_daily_summary
```

### Schedule Daily Summary (Windows Task Scheduler)
Create a scheduled task to run:
```
python C:\path\to\project\manage.py send_daily_summary
```

## Troubleshooting

### Common Issues
1. **Authentication failed**: Use App Password for Gmail, not regular password
2. **Connection refused**: Check SMTP settings and port
3. **SSL/TLS errors**: Verify `EMAIL_USE_TLS` setting

### Debug Mode
Add to settings for detailed email logs:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## Email Templates Location
Templates are in: `templates/emails/`
- `attendance_notification.html` - Admin notification
- `attendance_approved.html` - Employee approval
- `attendance_rejected.html` - Employee rejection
- `daily_attendance_summary.html` - Daily summary

## Customization
You can customize email templates by editing the HTML files in the templates/emails/ directory.
