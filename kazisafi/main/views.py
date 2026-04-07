from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Sum
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.http import JsonResponse, HttpResponse
from django.utils import timezone
from django.db.models import Sum, Count, Q
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime, timedelta
from .models import User, Employee, Attendance, Earning, Withdrawal, SupportTicket, AuditLog, PayrollSummary
from .forms import (
    CustomUserCreationForm, LoginForm, EmployeeForm, AttendanceForm, 
    WithdrawalForm, SupportTicketForm, EmployeeBulkCreateForm,
    AttendanceApprovalForm, WithdrawalProcessForm, SupportTicketResponseForm,
    UserProfileForm, PasswordChangeForm
)

# Helper functions
def is_admin(user):
    return user.is_authenticated and user.is_admin

def is_employee(user):
    return user.is_authenticated and user.is_employee

# Authentication Views
def login_view(request):
    """Handle user login"""
    print(f"Login request method: {request.method}")
    if request.method == 'POST':
        print(f"Login POST data: {dict(request.POST)}")
        form = LoginForm(request.POST)
        print(f"Login form valid: {form.is_valid()}")
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            print(f"Attempting login for: {username}")
            
            user = authenticate(username=username, password=password)
            if user:
                print(f"Login successful for: {user.username}")
                print(f"User details - is_admin: {user.is_admin}, is_employee: {user.is_employee}, is_staff: {user.is_staff}, is_superuser: {user.is_superuser}")
                login(request, user)
                
                # Log the login
                AuditLog.objects.create(
                    user=user,
                    action='login',
                    model_name='User',
                    object_id=user.id,
                    object_repr=str(user),
                    ip_address=request.META.get('REMOTE_ADDR'),
                    user_agent=request.META.get('HTTP_USER_AGENT', '')
                )
                
                if user.is_admin:
                    print("Redirecting to admin dashboard")
                    return redirect('admin_dashboard')
                else:
                    print("Redirecting to user dashboard")
                    return redirect('user_dashboard')
            else:
                print("Authentication failed")
                messages.error(request, 'Invalid username or password')
        else:
            print(f"Login form errors: {form.errors}")
    else:
        form = LoginForm()
        print("GET request - showing empty login form")
    
    return render(request, 'html/login.html', {'form': form})

def register_view(request):
    """Handle user registration"""
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            
            # Create employee profile
            Employee.objects.create(
                user=user,
                start_date=timezone.now().date(),
                status='active'
            )
            
            messages.success(request, 'Account created successfully! Please login.')
            return redirect('login')
        else:
            # Show form errors
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'html/register.html', {'form': form})

def logout_view(request):
    """Handle user logout"""
    if request.user.is_authenticated:
        AuditLog.objects.create(
            user=request.user,
            action='logout',
            model_name='User',
            object_id=request.user.id,
            object_repr=str(request.user),
            ip_address=request.META.get('REMOTE_ADDR'),
            user_agent=request.META.get('HTTP_USER_AGENT', '')
        )
        logout(request)
        messages.success(request, 'You have been logged out successfully.')
    return redirect('login')

# Admin Views
@user_passes_test(is_admin)
@login_required
def admin_dashboard(request):
    """Admin dashboard with statistics"""
    total_employees = User.objects.filter(is_employee=True).count()
    active_employees = Employee.objects.filter(status='active').count()
    pending_attendance = Attendance.objects.filter(status='pending').count()
    total_withdrawals = Withdrawal.objects.filter(status='completed').aggregate(
        total=Sum('amount'))['total'] or 0
    total_payroll = Earning.objects.aggregate(
        total=Sum('day_pay'))['total'] or 0
    
    # Recent activities
    recent_attendances = Attendance.objects.order_by('-created_at')[:5]
    recent_withdrawals = Withdrawal.objects.order_by('-created_at')[:5]
    
    # Create recent activities list
    recent_activities = []
    for attendance in recent_attendances:
        recent_activities.append({
            'type': 'attendance',
            'action': f'{attendance.employee.get_full_name()} marked attendance',
            'user': attendance.employee,
            'timestamp': attendance.created_at
        })
    for withdrawal in recent_withdrawals:
        recent_activities.append({
            'type': 'withdrawal',
            'action': f'{withdrawal.employee.get_full_name()} requested withdrawal',
            'user': withdrawal.employee,
            'timestamp': withdrawal.created_at
        })
    
    # Sort by timestamp
    recent_activities.sort(key=lambda x: x['timestamp'], reverse=True)
    recent_activities = recent_activities[:5]
    
    context = {
        'total_employees': total_employees,
        'active_employees': active_employees,
        'pending_attendance': pending_attendance,
        'total_withdrawals': total_withdrawals,
        'total_payroll': total_payroll,
        'recent_activities': recent_activities,
        'pending_attendances': Attendance.objects.filter(status='pending')[:5],
    }
    return render(request, 'html/admin-dashboard.html', context)

@user_passes_test(is_admin)
@login_required
def manage_employees(request):
    """Manage employees page"""
    employees = User.objects.filter(is_employee=True).select_related('employee_profile')
    return render(request, 'html/manage-employees.html', {'employees': employees})

@user_passes_test(is_admin)
@login_required
def admin_attendance(request):
    """Manage attendance for all employees"""
    attendances = Attendance.objects.all().select_related('employee').order_by('-date')
    
    # Statistics
    pending_count = attendances.filter(status='pending').count()
    approved_count = attendances.filter(status='approved').count()
    rejected_count = attendances.filter(status='rejected').count()
    
    context = {
        'attendances': attendances,
        'pending_count': pending_count,
        'approved_count': approved_count,
        'rejected_count': rejected_count,
    }
    return render(request, 'html/admin-attendance.html', context)

@user_passes_test(is_admin)
@login_required
def payroll_view(request):
    """Payroll and withdrawals overview"""
    # Calculate totals
    from django.db.models import Sum
    
    payroll_data = []
    employees = User.objects.filter(is_employee=True).select_related('employee_profile')
    
    for employee in employees:
        total_earned = Earning.objects.filter(employee=employee).aggregate(
            total=Sum('day_pay'))['total'] or 0
        
        total_withdrawn = Withdrawal.objects.filter(
            employee=employee, 
            status='completed'
        ).aggregate(total=Sum('amount'))['total'] or 0
        balance = total_earned - total_withdrawn
        
        payroll_data.append({
            'employee': employee,
            'total_earned': total_earned,
            'total_withdrawn': total_withdrawn,
            'balance': balance,
            'status': 'active' if balance > 0 else 'inactive'
        })
    
    # Overall totals
    total_payroll = sum(item['total_earned'] for item in payroll_data)
    total_withdrawn = sum(item['total_withdrawn'] for item in payroll_data)
    total_balance = sum(item['balance'] for item in payroll_data)
    
    context = {
        'payroll_data': payroll_data,
        'total_payroll': total_payroll,
        'total_withdrawn': total_withdrawn,
        'total_balance': total_balance,
    }
    return render(request, 'html/payroll.html', context)

@user_passes_test(is_admin)
@login_required
def audit_logs(request):
    """View system audit logs"""
    logs = AuditLog.objects.all().select_related('user').order_by('-timestamp')
    return render(request, 'html/audit-logs.html', {'logs': logs})

@user_passes_test(is_admin)
@login_required
def support_inbox(request):
    """Manage support tickets"""
    tickets = SupportTicket.objects.all().select_related('employee').order_by('-created_at')
    return render(request, 'html/support-inbox.html', {'tickets': tickets})

# User Views
@login_required
def user_dashboard(request):
    """User dashboard with personal stats"""
    user = request.user
    
    # Get user's statistics
    days_worked = Attendance.objects.filter(
        employee=user, status='approved'
    ).count()
    
    total_earned = Earning.objects.filter(employee=user).aggregate(
        total=Sum('day_pay'))['total'] or 0
    
    withdrawals = Withdrawal.objects.filter(
        employee=user, status='completed'
    ).aggregate(total=Sum('amount'))['total'] or 0
    
    balance = total_earned - withdrawals
    
    # Recent data
    recent_attendances = Attendance.objects.filter(
        employee=user
    ).order_by('-date')[:3]
    
    recent_withdrawals = Withdrawal.objects.filter(
        employee=user
    ).order_by('-created_at')[:2]
    
    context = {
        'days_worked': days_worked,
        'daily_rate': getattr(user.employee_profile, 'daily_rate', 0) if hasattr(user, 'employee_profile') else 0,
        'total_earned': total_earned,
        'balance': balance,
        'available_balance': balance,  # Add this for consistency
        'recent_attendances': recent_attendances,
        'recent_withdrawals': recent_withdrawals,
    }
    return render(request, 'html/user-dashboard.html', context)

@login_required
def user_attendance_view(request):
    """Mark and view attendance for logged-in user"""
    user = request.user
    today = timezone.now().date()
    
    # Get today's attendance
    today_attendance = Attendance.objects.filter(
        employee=user, date=today
    ).first()
    
    # Get attendance history
    attendance_history = Attendance.objects.filter(
        employee=user
    ).order_by('-date')[:30]
    
    # Get counts
    pending_count = Attendance.objects.filter(employee=user, status='pending').count()
    approved_count = Attendance.objects.filter(employee=user, status='approved').count()
    rejected_count = Attendance.objects.filter(employee=user, status='rejected').count()
    
    context = {
        'current_date': today,
        'current_time': timezone.now(),
        'today_attendance': today_attendance,
        'attendance_history': attendance_history,
        'pending_count': pending_count,
        'approved_count': approved_count,
        'rejected_count': rejected_count,
    }
    return render(request, 'html/userattendance.html', context)

@login_required
def user_earnings_view(request):
    """View earnings for logged-in user"""
    user = request.user
    
    # Calculate statistics
    days_worked = Attendance.objects.filter(
        employee=user, status='approved'
    ).count()
    
    daily_rate = getattr(user.employee_profile, 'daily_rate', 1500) if hasattr(user, 'employee_profile') else 1500
    total_earned = Earning.objects.filter(employee=user).aggregate(
        total=Sum('day_pay'))['total'] or 0
    
    total_withdrawn = Withdrawal.objects.filter(
        employee=user, status='completed'
    ).aggregate(total=Sum('amount'))['total'] or 0
    
    available_balance = total_earned - total_withdrawn
    
    # Get approved earnings for history
    approved_earnings = Earning.objects.filter(
        employee=user
    ).select_related('attendance').order_by('-date')
    
    context = {
        'days_worked': days_worked,
        'daily_rate': daily_rate,
        'total_earned': total_earned,
        'total_withdrawn': total_withdrawn,
        'available_balance': available_balance,
        'approved_earnings': approved_earnings,
    }
    return render(request, 'html/userearning.html', context)

@login_required
def user_withdraw_view(request):
    """Withdrawal page for logged-in user"""
    user = request.user
    
    # Calculate available balance
    total_earned = Earning.objects.filter(employee=user).aggregate(
        total=Sum('day_pay'))['total'] or 0
    
    total_withdrawn = Withdrawal.objects.filter(
        employee=user, status='completed'
    ).aggregate(total=Sum('amount'))['total'] or 0
    
    available_balance = total_earned - total_withdrawn
    
    # Get withdrawal history
    withdrawal_history = Withdrawal.objects.filter(
        employee=user
    ).order_by('-created_at')
    
    if request.method == 'POST':
        form = WithdrawalForm(request.POST)
        if form.is_valid():
            withdrawal = form.save(commit=False)
            withdrawal.employee = user
            withdrawal.phone_number = user.phone_number
            withdrawal.save()
            messages.success(request, 'Withdrawal request submitted successfully!')
            return redirect('user_withdraw')
    else:
        form = WithdrawalForm()
    
    context = {
        'form': form,
        'available_balance': available_balance,
        'withdrawal_history': withdrawal_history,
    }
    return render(request, 'html/userwithdraw.html', context)

@login_required
def contact_admin_view(request):
    """Contact admin support page"""
    print(f"Contact admin view - User: {request.user.username}, is_admin: {request.user.is_admin}, is_employee: {request.user.is_employee}")
    
    if request.method == 'POST':
        form = SupportTicketForm(request.POST)
        if form.is_valid():
            # Check user role before saving ticket
            print(f"Before ticket save - User: {request.user.username}, is_admin: {request.user.is_admin}, is_employee: {request.user.is_employee}")
            
            ticket = form.save(commit=False)
            ticket.employee = request.user
            ticket.save()
            
            # Check user role after saving ticket
            print(f"After ticket save - User: {request.user.username}, is_admin: {request.user.is_admin}, is_employee: {request.user.is_employee}")
            
            # Refresh user from database to check if role changed
            request.user.refresh_from_db()
            print(f"After refresh - User: {request.user.username}, is_admin: {request.user.is_admin}, is_employee: {request.user.is_employee}")
            
            messages.success(request, 'Support ticket submitted successfully!')
            return redirect('contact_admin')
    else:
        form = SupportTicketForm()
    
    return render(request, 'html/contactadmin.html', {'form': form})

# AJAX Views
@login_required
def mark_attendance_ajax(request):
    """AJAX endpoint for marking attendance"""
    if request.method == 'POST':
        user = request.user
        today = timezone.now().date()
        
        # Check if already marked
        existing = Attendance.objects.filter(employee=user, date=today).first()
        if existing:
            return JsonResponse({'status': 'error', 'message': 'Attendance already marked for today'})
        
        # Create attendance record
        attendance = Attendance.objects.create(
            employee=user,
            date=today,
            check_in=timezone.now(),
            status='pending'
        )
        
        # Create earning record
        daily_rate = getattr(user.employee_profile, 'daily_rate', 1500) if hasattr(user, 'employee_profile') else 1500
        Earning.objects.create(
            employee=user,
            attendance=attendance,
            date=today,
            daily_rate=daily_rate,
            day_pay=daily_rate
        )
        
        # Log the action
        AuditLog.objects.create(
            user=user,
            action='create',
            model_name='Attendance',
            object_id=attendance.id,
            object_repr=str(attendance),
            ip_address=request.META.get('REMOTE_ADDR'),
            user_agent=request.META.get('HTTP_USER_AGENT', '')
        )
        
        return JsonResponse({'status': 'success', 'message': 'Attendance marked successfully'})
    
    return JsonResponse({'status': 'error', 'message': 'Invalid request'})

@login_required
def approve_attendance_ajax(request):
    """AJAX endpoint for approving attendance and calculating earnings"""
    if request.method == 'POST':
        if not request.user.is_admin:
            return JsonResponse({'status': 'error', 'message': 'Unauthorized'})
        
        attendance_id = request.POST.get('attendance_id')
        try:
            attendance = Attendance.objects.get(id=attendance_id)
            
            if attendance.status != 'pending':
                return JsonResponse({'status': 'error', 'message': 'Attendance already processed'})
            
            # Calculate work hours and earnings
            if attendance.check_in and attendance.check_out:
                # Calculate work hours
                check_in = attendance.check_in
                check_out = attendance.check_out
                
                # Calculate total work hours
                total_seconds = (check_out - check_in).total_seconds()
                work_hours = total_seconds / 3600  # Convert to hours
                
                # Calculate overtime (after 8 hours = regular time)
                regular_hours = min(work_hours, 8)
                overtime_hours = max(work_hours - 8, 0)
                
                # Update attendance with calculated hours
                attendance.overtime_hours = overtime_hours
                attendance.status = 'approved'
                attendance.save()
                
                # Get daily rate
                daily_rate = getattr(attendance.employee.employee_profile, 'daily_rate', 1500) if hasattr(attendance.employee, 'employee_profile') else 1500
                hourly_rate = daily_rate / 8  # Regular hourly rate
                overtime_rate = hourly_rate * 1.5  # 1.5x for overtime
                
                # Calculate earnings
                regular_pay = regular_hours * hourly_rate
                overtime_pay = overtime_hours * overtime_rate
                total_pay = regular_pay + overtime_pay
                
                # Update or create earning record
                earning, created = Earning.objects.update_or_create(
                    attendance=attendance,
                    employee=attendance.employee,
                    date=attendance.date,
                    defaults={
                        'daily_rate': daily_rate,
                        'overtime_hours': overtime_hours,
                        'overtime_rate': overtime_rate,
                        'day_pay': total_pay
                    }
                )
                
                return JsonResponse({
                    'status': 'success',
                    'message': 'Attendance approved successfully',
                    'data': {
                        'work_hours': round(work_hours, 2),
                        'regular_hours': round(regular_hours, 2),
                        'overtime_hours': round(overtime_hours, 2),
                        'regular_pay': round(regular_pay, 2),
                        'overtime_pay': round(overtime_pay, 2),
                        'total_pay': round(total_pay, 2)
                    }
                })
            else:
                # Approve without check-out time (use default 8 hours)
                attendance.status = 'approved'
                attendance.save()
                
                daily_rate = getattr(attendance.employee.employee_profile, 'daily_rate', 1500) if hasattr(attendance.employee, 'employee_profile') else 1500
                
                earning, created = Earning.objects.update_or_create(
                    attendance=attendance,
                    employee=attendance.employee,
                    date=attendance.date,
                    defaults={
                        'daily_rate': daily_rate,
                        'overtime_hours': 0,
                        'overtime_rate': 0,
                        'day_pay': daily_rate
                    }
                )
                
                return JsonResponse({
                    'status': 'success',
                    'message': 'Attendance approved (8 hours default)',
                    'data': {
                        'work_hours': 8.0,
                        'regular_hours': 8.0,
                        'overtime_hours': 0.0,
                        'regular_pay': daily_rate,
                        'overtime_pay': 0,
                        'total_pay': daily_rate
                    }
                })
                
        except Attendance.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Attendance not found'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    
    return JsonResponse({'status': 'error', 'message': 'Invalid request'})

@login_required
def reject_attendance_ajax(request):
    """AJAX endpoint for rejecting attendance"""
    if request.method == 'POST':
        if not request.user.is_admin:
            return JsonResponse({'status': 'error', 'message': 'Unauthorized'})
        
        attendance_id = request.POST.get('attendance_id')
        try:
            attendance = Attendance.objects.get(id=attendance_id)
            
            if attendance.status != 'pending':
                return JsonResponse({'status': 'error', 'message': 'Attendance already processed'})
            
            attendance.status = 'rejected'
            attendance.save()
            
            return JsonResponse({
                'status': 'success',
                'message': 'Attendance rejected successfully'
            })
            
        except Attendance.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Attendance not found'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    
    return JsonResponse({'status': 'error', 'message': 'Invalid request'})

@login_required
def process_withdrawal_ajax(request):
    """AJAX endpoint for processing withdrawal"""
    if request.method == 'POST':
        user = request.user
        amount = request.POST.get('amount')
        
        # Validate balance
        total_earned = Earning.objects.filter(employee=user).aggregate(
            total=Sum('day_pay'))['total'] or 0
        
        total_withdrawn = Withdrawal.objects.filter(
            employee=user, status='completed'
        ).aggregate(total=Sum('amount'))['total'] or 0
        
        available_balance = total_earned - total_withdrawn
        
        if float(amount) > available_balance:
            return JsonResponse({'status': 'error', 'message': 'Insufficient balance'})
        
        # Create withdrawal
        withdrawal = Withdrawal.objects.create(
            employee=user,
            amount=amount,
            phone_number=user.phone_number,
            status='pending'
        )
        
        # Log the action
        AuditLog.objects.create(
            user=user,
            action='create',
            model_name='Withdrawal',
            object_id=withdrawal.id,
            object_repr=str(withdrawal),
            ip_address=request.META.get('REMOTE_ADDR'),
            user_agent=request.META.get('HTTP_USER_AGENT', '')
        )
        
        return JsonResponse({'status': 'success', 'message': 'Withdrawal request submitted'})
    
    return JsonResponse({'status': 'error', 'message': 'Invalid request'})

@csrf_exempt
@login_required
def user_attendance_history_ajax(request):
    """AJAX endpoint for user attendance history"""
    if request.method == 'GET':
        user = request.user
        attendances = Attendance.objects.filter(
            employee=user
        ).order_by('-date').values(
            'date', 'check_in', 'check_out', 'status'
        )
        
        return JsonResponse({
            'status': 'success',
            'data': list(attendances)
        })
    
    return JsonResponse({'status': 'error', 'message': 'Invalid request'})

@csrf_exempt
@login_required
def user_withdrawal_history_ajax(request):
    """AJAX endpoint for user withdrawal history"""
    if request.method == 'GET':
        user = request.user
        withdrawals = Withdrawal.objects.filter(
            employee=user
        ).order_by('-created_at').values(
            'id', 'amount', 'status', 'created_at'
        )
        
        return JsonResponse({
            'status': 'success',
            'data': list(withdrawals)
        })
    
    return JsonResponse({'status': 'error', 'message': 'Invalid request'})

@csrf_exempt
@login_required
def withdrawal_status_ajax(request, withdrawal_id):
    """AJAX endpoint for withdrawal status"""
    if request.method == 'GET':
        try:
            withdrawal = Withdrawal.objects.get(id=withdrawal_id, employee=request.user)
            return JsonResponse({
                'status': 'success',
                'data': {
                    'id': withdrawal.id,
                    'status': withdrawal.status,
                    'amount': float(withdrawal.amount)
                }
            })
        except Withdrawal.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Withdrawal not found'})
    
    return JsonResponse({'status': 'error', 'message': 'Invalid request'})

@csrf_exempt
@login_required
def withdrawal_updates_ajax(request):
    """AJAX endpoint for withdrawal updates"""
    if request.method == 'GET':
        user = request.user
        recent_withdrawals = Withdrawal.objects.filter(
            employee=user,
            status__in=['pending', 'processing']
        ).order_by('-created_at')[:5]
        
        return JsonResponse({
            'status': 'success',
            'has_updates': len(recent_withdrawals) > 0,
            'data': list(recent_withdrawals)
        })
    
    return JsonResponse({'status': 'error', 'message': 'Invalid request'})
