# Kazi Safi Email Setup

## Current Configuration

**App Name**: Kazi Safi  
**Admin Email**: vivianmukhongo72@gmail.com  
**Current Status**: Development (Console Backend)

## Quick Setup for Production

### Step 1: Generate Gmail App Password

1. **Enable 2-Factor Authentication** on your Gmail account
2. Go to: https://myaccount.google.com/apppasswords
3. Select "Mail" and "Other (Custom name)"
4. Enter "Kazi Safi" as the app name
5. Copy the 16-character password (no spaces)

### Step 2: Update Settings

Edit `kazisafi/settings.py`:

```python
# Comment out this line:
# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Uncomment these lines:
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'vivianmukhongo72@gmail.com'
EMAIL_HOST_PASSWORD = 'your-16-character-app-password'
DEFAULT_FROM_EMAIL = 'vivianmukhongo72@gmail.com'
```

### Step 3: Test Configuration

```bash
python manage.py test_email
```

## Email Features for Kazi Safi

### 1. Admin Notifications
- **Trigger**: Employee marks attendance
- **Recipient**: vivianmukhongo72@gmail.com
- **Content**: Employee details, check-in time, approval link

### 2. Employee Notifications
- **Approval**: When you approve attendance
- **Rejection**: When you reject attendance (with reason)

### 3. Daily Summary
- **Command**: `python manage.py send_daily_summary`
- **Content**: All pending attendance for the day

## Switch Between Backends

```bash
# Switch to SMTP (production)
python manage.py switch_email smtp

# Switch to Console (development)
python manage.py switch_email console
```

## Test Email Flow

1. **Employee marks attendance** 
   - You receive email at vivianmukhongo72@gmail.com
   - Email contains direct link to approve

2. **You approve attendance**
   - Employee receives approval notification
   - Earnings calculated automatically

3. **You reject attendance**
   - Employee receives rejection with reason
   - Can contact you for clarification

## Current Status

**Working Now**: 
- All email functionality ready
- Beautiful HTML templates
- Console emails (prints to terminal)

**Ready for Production**:
- Just configure SMTP with app password
- All emails will be sent to vivianmukhongo72@gmail.com

## Troubleshooting

**"Bad Credentials" Error**:
- Use App Password, not regular Gmail password
- App password must be 16 characters
- No spaces in the password

**No Email Received**:
- Check spam folder
- Verify SMTP settings
- Test with: `python manage.py test_email`

## Security Notes

- Never commit real passwords to Git
- Use environment variables in production
- Keep app passwords secure

The Kazi Safi email system is fully configured and ready!
