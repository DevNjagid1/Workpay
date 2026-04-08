from django.core.mail import send_mail, mail_admins
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags


def send_attendance_notification(attendance):
    """
    Send email notification to admin when attendance is marked and needs approval
    """
    subject = f'New Attendance Marked - {attendance.employee.username}'
    
    # Create email context
    context = {
        'employee': attendance.employee,
        'attendance': attendance,
        'check_in_time': attendance.check_in.strftime('%I:%M %p') if attendance.check_in else 'N/A',
        'date': attendance.date.strftime('%B %d, %Y'),
        'status': attendance.status,
    }
    
    # Render HTML email template
    html_message = render_to_string('emails/attendance_notification.html', context)
    
    # Plain text version
    plain_message = strip_tags(html_message)
    plain_message = f"""
    New Attendance Marked - Action Required

    Employee: {attendance.employee.username}
    Date: {attendance.date.strftime('%B %d, %Y')}
    Check-in Time: {attendance.check_in.strftime('%I:%M %p') if attendance.check_in else 'N/A'}
    Status: {attendance.status}

    Please review and approve this attendance in the admin dashboard.
    
    Admin Dashboard: http://127.0.0.1:8000/admin/attendance/
    """
    
    # Send email to notification address
    try:
        send_mail(
            subject=subject,
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[settings.NOTIFICATION_EMAIL],
            html_message=html_message,
            fail_silently=False,
        )
        print(f"Attendance notification sent for {attendance.employee.username}")
        return True
    except Exception as e:
        print(f"Failed to send attendance notification: {str(e)}")
        return False


def send_attendance_approval_notification(attendance, approved_by):
    """
    Send email to employee when their attendance is approved
    """
    subject = f'Attendance Approved - {attendance.date.strftime("%B %d, %Y")}'
    
    context = {
        'employee': attendance.employee,
        'attendance': attendance,
        'approved_by': approved_by,
        'date': attendance.date.strftime('%B %d, %Y'),
        'check_in_time': attendance.check_in.strftime('%I:%M %p') if attendance.check_in else 'N/A',
        'check_out_time': attendance.check_out.strftime('%I:%M %p') if attendance.check_out else 'N/A',
    }
    
    html_message = render_to_string('emails/attendance_approved.html', context)
    plain_message = strip_tags(html_message)
    
    try:
        send_mail(
            subject=subject,
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[attendance.employee.email],
            html_message=html_message,
            fail_silently=False,
        )
        print(f"Attendance approval sent to {attendance.employee.username}")
        return True
    except Exception as e:
        print(f"Failed to send attendance approval: {str(e)}")
        return False


def send_attendance_rejection_notification(attendance, rejected_by, reason):
    """
    Send email to employee when their attendance is rejected
    """
    subject = f'Attendance Rejected - {attendance.date.strftime("%B %d, %Y")}'
    
    context = {
        'employee': attendance.employee,
        'attendance': attendance,
        'rejected_by': rejected_by,
        'reason': reason,
        'date': attendance.date.strftime('%B %d, %Y'),
        'check_in_time': attendance.check_in.strftime('%I:%M %p') if attendance.check_in else 'N/A',
    }
    
    html_message = render_to_string('emails/attendance_rejected.html', context)
    plain_message = strip_tags(html_message)
    
    try:
        send_mail(
            subject=subject,
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[attendance.employee.email],
            html_message=html_message,
            fail_silently=False,
        )
        print(f"Attendance rejection sent to {attendance.employee.username}")
        return True
    except Exception as e:
        print(f"Failed to send attendance rejection: {str(e)}")
        return False


def send_daily_attendance_summary():
    """
    Send daily summary of all pending attendance to admin
    """
    from main.models import Attendance
    
    pending_attendance = Attendance.objects.filter(status='pending')
    
    if not pending_attendance.exists():
        return False
    
    subject = f'Daily Attendance Summary - {pending_attendance.count()} Pending Approvals'
    
    context = {
        'pending_attendance': pending_attendance,
        'total_pending': pending_attendance.count(),
        'date': pending_attendance.first().date if pending_attendance.exists() else None,
    }
    
    html_message = render_to_string('emails/daily_attendance_summary.html', context)
    plain_message = strip_tags(html_message)
    
    try:
        send_mail(
            subject=subject,
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[settings.NOTIFICATION_EMAIL],
            html_message=html_message,
            fail_silently=False,
        )
        print(f"Daily attendance summary sent - {pending_attendance.count()} pending")
        return True
    except Exception as e:
        print(f"Failed to send daily summary: {str(e)}")
        return False
