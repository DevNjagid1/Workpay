from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

class User(AbstractUser):
    """Extended User model for Kazi Safi system"""
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    employee_id = models.CharField(max_length=20, unique=True, blank=True, null=True)
    daily_rate = models.DecimalField(max_digits=10, decimal_places=2, default=1500.00)
    is_employee = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.get_full_name() or self.username} ({self.employee_id})"
    
    def get_full_name(self):
        """Return the user's full name"""
        return f"{self.first_name} {self.last_name}".strip() or self.username

class Employee(models.Model):
    """Employee profile with additional details"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='employee_profile')
    start_date = models.DateField()
    status = models.CharField(max_length=20, choices=[
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('suspended', 'Suspended')
    ], default='active')
    department = models.CharField(max_length=100, blank=True)
    position = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.status}"

class Attendance(models.Model):
    """Attendance records for employees"""
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected')
    ]
    
    employee = models.ForeignKey(User, on_delete=models.CASCADE, related_name='attendances')
    date = models.DateField()
    check_in = models.DateTimeField(null=True, blank=True)
    check_out = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    overtime_hours = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['employee', 'date']

    def __str__(self):
        return f"{self.employee.get_full_name()} - {self.date} ({self.status})"

class Earning(models.Model):
    """Daily earnings calculation for approved attendance"""
    attendance = models.OneToOneField(Attendance, on_delete=models.CASCADE, related_name='earning')
    employee = models.ForeignKey(User, on_delete=models.CASCADE, related_name='earnings')
    date = models.DateField()
    daily_rate = models.DecimalField(max_digits=10, decimal_places=2)
    overtime_hours = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    overtime_rate = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    day_pay = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.employee.get_full_name()} - {self.date} (KES {self.day_pay})"

class Withdrawal(models.Model):
    """Withdrawal requests via M-Pesa"""
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('failed', 'Failed')
    ]
    
    employee = models.ForeignKey(User, on_delete=models.CASCADE, related_name='withdrawals')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    receipt_number = models.CharField(max_length=50, blank=True, null=True)
    mpesa_transaction_id = models.CharField(max_length=50, blank=True, null=True)
    phone_number = models.CharField(max_length=20)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    processed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.employee.get_full_name()} - KES {self.amount} ({self.status})"

class SupportTicket(models.Model):
    """Support tickets from employees"""
    STATUS_CHOICES = [
        ('open', 'Open'),
        ('in_progress', 'In Progress'),
        ('resolved', 'Resolved'),
        ('closed', 'Closed')
    ]
    
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('urgent', 'Urgent')
    ]
    
    CATEGORY_CHOICES = [
        ('salary', 'Salary Inquiry'),
        ('attendance', 'Attendance Issue'),
        ('technical', 'Technical Support'),
        ('other', 'Other')
    ]
    
    employee = models.ForeignKey(User, on_delete=models.CASCADE, related_name='support_tickets')
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='other')
    subject = models.CharField(max_length=200)
    message = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='open')
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='medium')
    admin_response = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    resolved_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"#{self.id} - {self.subject} ({self.status})"

class AuditLog(models.Model):
    """System audit logs for tracking admin actions"""
    ACTION_CHOICES = [
        ('create', 'Create'),
        ('update', 'Update'),
        ('delete', 'Delete'),
        ('approve', 'Approve'),
        ('reject', 'Reject'),
        ('login', 'Login'),
        ('logout', 'Logout')
    ]
    
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='audit_logs')
    action = models.CharField(max_length=20, choices=ACTION_CHOICES)
    model_name = models.CharField(max_length=50)
    object_id = models.PositiveIntegerField(null=True, blank=True)
    object_repr = models.CharField(max_length=200, blank=True)
    details = models.JSONField(default=dict)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.action} - {self.model_name} at {self.timestamp}"

class PayrollSummary(models.Model):
    """Monthly payroll summary for reporting"""
    employee = models.ForeignKey(User, on_delete=models.CASCADE, related_name='payroll_summaries')
    month = models.DateField()
    days_worked = models.PositiveIntegerField(default=0)
    total_earned = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total_withdrawn = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    overtime_hours = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    overtime_pay = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['employee', 'month']

    def __str__(self):
        return f"{self.employee.get_full_name()} - {self.month.strftime('%B %Y')}"

class SystemSettings(models.Model):
    """Global system settings"""
    minimum_withdrawal = models.DecimalField(max_digits=10, decimal_places=2, default=50.00)
    overtime_rate_multiplier = models.DecimalField(max_digits=3, decimal_places=2, default=1.5)
    working_hours_per_day = models.DecimalField(max_digits=3, decimal_places=2, default=8.0)
    currency = models.CharField(max_length=3, default='KES')
    company_name = models.CharField(max_length=100, default='Kazi Safi')
    mpesa_paybill = models.CharField(max_length=10, blank=True)
    mpesa_account_number = models.CharField(max_length=20, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Settings - {self.company_name}"
