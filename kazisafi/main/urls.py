from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Authentication URLs
    path('', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    
    # Admin URLs
    path('admin/', views.admin_dashboard, name='admin_dashboard'),
    path('admin/employees/', views.manage_employees, name='manage_employees'),
    path('admin/attendance/', views.admin_attendance, name='admin_attendance'),
    path('admin/payroll/', views.payroll_view, name='payroll'),
    path('admin/audit-logs/', views.audit_logs, name='audit_logs'),
    path('admin/support/', views.support_inbox, name='support_inbox'),
    
    # User URLs
    path('dashboard/', views.user_dashboard, name='user_dashboard'),
    path('attendance/', views.user_attendance_view, name='user_attendance'),
    path('earnings/', views.user_earnings_view, name='user_earnings'),
    path('withdraw/', views.user_withdraw_view, name='user_withdraw'),
    path('contact-admin/', views.contact_admin_view, name='contact_admin'),
    
    # AJAX URLs
    path('api/mark-attendance/', views.mark_attendance_ajax, name='mark_attendance_ajax'),
    path('api/approve-attendance/', views.approve_attendance_ajax, name='approve_attendance_ajax'),
    path('api/reject-attendance/', views.reject_attendance_ajax, name='reject_attendance_ajax'),
    path('api/process-withdrawal/', views.process_withdrawal_ajax, name='process_withdrawal_ajax'),
    path('api/user-attendance-history/', views.user_attendance_history_ajax, name='user_attendance_history_ajax'),
    path('api/user-withdrawal-history/', views.user_withdrawal_history_ajax, name='user_withdrawal_history_ajax'),
    path('api/withdrawal-status/<int:withdrawal_id>/', views.withdrawal_status_ajax, name='withdrawal_status_ajax'),
    path('api/withdrawal-updates/', views.withdrawal_updates_ajax, name='withdrawal_updates_ajax'),
    
    # Django Auth URLs
    path('password-reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]
