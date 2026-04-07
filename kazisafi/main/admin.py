from django.contrib import admin
from .models import User, Employee, Attendance, Earning, Withdrawal, SupportTicket, AuditLog, PayrollSummary, SystemSettings

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'first_name', 'last_name', 'email', 'employee_id', 'is_admin', 'is_employee', 'date_joined']
    list_filter = ['is_admin', 'is_employee', 'date_joined']
    search_fields = ['username', 'first_name', 'last_name', 'email', 'employee_id']
    ordering = ['-date_joined']

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ['user', 'start_date', 'status', 'department', 'position']
    list_filter = ['status', 'department', 'start_date']
    search_fields = ['user__username', 'user__first_name', 'user__last_name']
    ordering = ['-start_date']

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ['employee', 'date', 'check_in', 'check_out', 'status', 'overtime_hours']
    list_filter = ['status', 'date']
    search_fields = ['employee__username', 'employee__first_name', 'employee__last_name']
    date_hierarchy = 'date'
    ordering = ['-date']

@admin.register(Earning)
class EarningAdmin(admin.ModelAdmin):
    list_display = ['employee', 'date', 'daily_rate', 'overtime_hours', 'day_pay']
    list_filter = ['date']
    search_fields = ['employee__username', 'employee__first_name', 'employee__last_name']
    date_hierarchy = 'date'
    ordering = ['-date']

@admin.register(Withdrawal)
class WithdrawalAdmin(admin.ModelAdmin):
    list_display = ['employee', 'amount', 'status', 'receipt_number', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['employee__username', 'employee__first_name', 'employee__last_name', 'receipt_number']
    ordering = ['-created_at']

@admin.register(SupportTicket)
class SupportTicketAdmin(admin.ModelAdmin):
    list_display = ['employee', 'subject', 'priority', 'status', 'created_at']
    list_filter = ['priority', 'status', 'created_at']
    search_fields = ['employee__username', 'employee__first_name', 'employee__last_name', 'subject']
    ordering = ['-created_at']

@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ['user', 'action', 'model_name', 'object_repr', 'ip_address', 'timestamp']
    list_filter = ['action', 'model_name', 'timestamp']
    search_fields = ['user__username', 'action', 'model_name', 'object_repr']
    date_hierarchy = 'timestamp'
    ordering = ['-timestamp']
    readonly_fields = ['user', 'action', 'model_name', 'object_id', 'object_repr', 'ip_address', 'user_agent', 'timestamp']

@admin.register(PayrollSummary)
class PayrollSummaryAdmin(admin.ModelAdmin):
    list_display = ['employee', 'month', 'days_worked', 'total_earned', 'total_withdrawn', 'balance', 'created_at']
    list_filter = ['month', 'created_at']
    date_hierarchy = 'month'
    ordering = ['-month']
    readonly_fields = ['employee', 'month', 'days_worked', 'total_earned', 'total_withdrawn', 'balance', 'overtime_hours', 'overtime_pay', 'created_at']

@admin.register(SystemSettings)
class SystemSettingsAdmin(admin.ModelAdmin):
    list_display = ['company_name', 'currency', 'minimum_withdrawal', 'overtime_rate_multiplier', 'working_hours_per_day', 'updated_at']
    search_fields = ['company_name']
    ordering = ['company_name']
