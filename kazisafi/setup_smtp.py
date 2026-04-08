#!/usr/bin/env python
"""
SMTP Setup Script for Kazi Safi
Run this script to configure email settings for production
"""

import os
import sys

def setup_gmail_smtp():
    """Setup Gmail SMTP configuration"""
    print("=== Gmail SMTP Setup ===")
    print("1. Enable 2-factor authentication on your Gmail account")
    print("2. Go to: https://myaccount.google.com/apppasswords")
    print("3. Generate an app password for 'Kazi Safi'")
    print("4. Copy the app password (16 characters)")
    
    email = input("Enter your Gmail address: ").strip()
    app_password = input("Enter your 16-character app password: ").strip()
    
    if not email or not app_password:
        print("Error: Email and app password are required")
        return False
    
    # Update settings.py
    settings_file = 'kazisafi/settings.py'
    
    try:
        with open(settings_file, 'r') as f:
            content = f.read()
        
        # Replace console backend with SMTP
        content = content.replace(
            "EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'",
            "EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'"
        )
        
        # Uncomment and update SMTP settings
        lines = content.split('\n')
        new_lines = []
        
        for line in lines:
            if line.strip() == "# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'":
                new_lines.append("EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'")
            elif line.strip() == "# EMAIL_HOST = 'smtp.gmail.com'":
                new_lines.append("EMAIL_HOST = 'smtp.gmail.com'")
            elif line.strip() == "# EMAIL_PORT = 587":
                new_lines.append("EMAIL_PORT = 587")
            elif line.strip() == "# EMAIL_USE_TLS = True":
                new_lines.append("EMAIL_USE_TLS = True")
            elif line.strip() == "# EMAIL_HOST_USER = 'your-email@gmail.com'":
                new_lines.append(f"EMAIL_HOST_USER = '{email}'")
            elif line.strip() == "# EMAIL_HOST_PASSWORD = 'your-app-password'":
                new_lines.append(f"EMAIL_HOST_PASSWORD = '{app_password}'")
            elif line.strip() == "# DEFAULT_FROM_EMAIL = 'your-email@gmail.com'":
                new_lines.append(f"DEFAULT_FROM_EMAIL = '{email}'")
            elif line.strip() == "# NOTIFICATION_EMAIL = 'admin@kazisafi.com'":
                new_lines.append(f"NOTIFICATION_EMAIL = '{email}'")
            else:
                new_lines.append(line)
        
        with open(settings_file, 'w') as f:
            f.write('\n'.join(new_lines))
        
        print(f"SMTP configured successfully for {email}")
        return True
        
    except Exception as e:
        print(f"Error updating settings: {e}")
        return False

def test_email_config():
    """Test email configuration"""
    print("\n=== Testing Email Configuration ===")
    
    try:
        os.system("python manage.py test_email")
        return True
    except Exception as e:
        print(f"Error testing email: {e}")
        return False

def main():
    print("Kazi Safi SMTP Setup")
    print("====================")
    
    choice = input("\nChoose email provider:\n1. Gmail\n2. Outlook/Hotmail\n3. SendGrid\n4. Test current config\n5. Exit\n\nChoice (1-5): ").strip()
    
    if choice == '1':
        if setup_gmail_smtp():
            test_email_config()
    elif choice == '2':
        print("\nOutlook/Hotmail Setup:")
        print("1. Use your Outlook email and password")
        print("2. Update settings.py manually with:")
        print("   EMAIL_HOST = 'smtp-mail.outlook.com'")
        print("   EMAIL_PORT = 587")
        print("   EMAIL_USE_TLS = True")
    elif choice == '3':
        print("\nSendGrid Setup:")
        print("1. Create SendGrid account")
        print("2. Generate API key")
        print("3. Update settings.py with:")
        print("   EMAIL_HOST = 'smtp.sendgrid.net'")
        print("   EMAIL_HOST_USER = 'apikey'")
        print("   EMAIL_HOST_PASSWORD = 'your-sendgrid-api-key'")
    elif choice == '4':
        test_email_config()
    elif choice == '5':
        print("Goodbye!")
    else:
        print("Invalid choice")

if __name__ == '__main__':
    main()
