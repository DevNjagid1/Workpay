# SMTP Email Setup Guide for Kazi Safi

## Quick Setup Steps

### Option 1: Gmail (Recommended)

1. **Enable 2-Factor Authentication**
   - Go to: https://myaccount.google.com/security
   - Enable 2-Step Verification

2. **Generate App Password for Kazi Safi**
   - Go to: https://myaccount.google.com/apppasswords
   - Select "Mail" and "Other (Custom name)"
   - Enter "Kazi Safi" as the name
   - Copy the 16-character password (no spaces)

3. **Update Settings**
   Edit `kazisafi/settings.py`:
   ```python
   # Comment out this line:
   # EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
   
   # Uncomment these lines:
   EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
   EMAIL_HOST = 'smtp.gmail.com'
   EMAIL_PORT = 587
   EMAIL_USE_TLS = True
   EMAIL_HOST_USER = 'vivmukhongo@gmail.com'
   EMAIL_HOST_PASSWORD = 'wtdgafpwnizcrtst'
   DEFAULT_FROM_EMAIL = 'vivianmukhongo72@gmail.com'
   ```

### Option 2: Outlook/Hotmail

1. **Update Settings**
   ```python
   EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
   EMAIL_HOST = 'smtp-mail.outlook.com'
   EMAIL_PORT = 587
   EMAIL_USE_TLS = True
   EMAIL_HOST_USER = 'your-email@outlook.com'
   EMAIL_HOST_PASSWORD = 'your-password'
   DEFAULT_FROM_EMAIL = 'your-email@outlook.com'
   ```

### Option 3: SendGrid

1. **Create SendGrid Account**
   - Sign up at: https://sendgrid.com/
   - Verify your email address

2. **Generate API Key**
   - Go to Settings > API Keys
   - Create API Key with "Full Access"
   - Copy the API key

3. **Update Settings**
   ```python
   EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
   EMAIL_HOST = 'smtp.sendgrid.net'
   EMAIL_PORT = 587
   EMAIL_USE_TLS = True
   EMAIL_HOST_USER = 'apikey'
   EMAIL_HOST_PASSWORD = 'your-sendgrid-api-key'
   DEFAULT_FROM_EMAIL = 'your-email@yourdomain.com'
   ```

## Test Your Configuration

```bash
python manage.py test_email
```

## Troubleshooting

### Gmail Issues
- **"Bad Credentials"**: Use App Password, not regular password
- **"Less secure app"**: Enable 2-factor authentication first
- **App Password must be 16 characters** with no spaces

### General Issues
- **Check firewall**: Port 587 must be open
- **Check antivirus**: May block SMTP connections
- **Verify credentials**: Email and password must be exact

### Debug Mode
Add to settings for detailed logs:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## Switch Back to Development
To switch back to console emails (for testing):
```python
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
```

## Email Features Once Configured

1. **Admin Notifications**: When employees mark attendance
2. **Employee Notifications**: When attendance is approved/rejected
3. **Daily Summaries**: Automated daily attendance reports
4. **Professional Templates**: Beautiful HTML email designs

## Security Notes

- Never commit real passwords to version control
- Use environment variables in production:
  ```python
  import os
  EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_PASSWORD')
  ```
- Consider using Django-environ for configuration management
