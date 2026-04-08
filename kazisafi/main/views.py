import json
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

# ── Helpers ──────────────────────────────────────────────────────────────────
def is_admin(user):
    return user.is_authenticated and user.is_admin

def is_employee(user):
    return user.is_authenticated and user.is_employee

def _parse_json_body(request):
    """Safely parse a JSON request body. Returns a dict (may be empty)."""
    try:
        return json.loads(request.body)
    except (json.JSONDecodeError, ValueError):
        return {}

# ── Authentication ────────────────────────────────────────────────────────────
def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password']
            )
            if user:
                login(request, user)
                AuditLog.objects.create(
                    user=user, action='login', model_name='User',
                    object_id=user.id, object_repr=str(user),
                    ip_address=request.META.get('REMOTE_ADDR'),
                    user_agent=request.META.get('HTTP_USER_AGENT', '')
                )
                return redirect('admin_dashboard' if user.is_admin else 'user_dashboard')
            messages.error(request, 'Invalid username or password')
    else:
        form = LoginForm()
    return render(request, 'html/login.html', {'form': form})


def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            Employee.objects.create(user=user, start_date=timezone.now().date(), status='active')
            messages.success(request, 'Account created successfully! Please login.')
            return redirect('login')
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(request, f'{field}: {error}')
    else:
        form = CustomUserCreationForm()
    return render(request, 'html/register.html', {'form': form})


def logout_view(request):
    if request.user.is_authenticated:
        AuditLog.objects.create(
            user=request.user, action='logout', model_name='User',
            object_id=request.user.id, object_repr=str(request.user),
            ip_address=request.META.get('REMOTE_ADDR'),
            user_agent=request.META.get('HTTP_USER_AGENT', '')
        )
        logout(request)
        messages.success(request, 'You have been logged out successfully.')
    return redirect('login')


# ── Admin Views ───────────────────────────────────────────────────────────────
@user_passes_test(is_admin)
@login_required
def admin_dashboard(request):
    total_employees   = User.objects.filter(is_employee=True).count()
    active_employees  = Employee.objects.filter(status='active').count() if Employee.objects.exists() else 0
    pending_attendance = Attendance.objects.filter(status='pending').count()
    total_withdrawals = Withdrawal.objects.filter(status='completed').aggregate(total=Sum('amount'))['total'] or 0
    total_payroll     = Earning.objects.aggregate(total=Sum('day_pay'))['total'] or 0

    recent_attendances = Attendance.objects.order_by('-created_at')[:5]
    recent_withdrawals = Withdrawal.objects.order_by('-created_at')[:5]

    recent_activities = []
    for a in recent_attendances:
        recent_activities.append({'type': 'attendance', 'action': f'{a.employee.get_full_name()} marked attendance', 'user': a.employee, 'timestamp': a.created_at})
    for w in recent_withdrawals:
        recent_activities.append({'type': 'withdrawal', 'action': f'{w.employee.get_full_name()} requested withdrawal', 'user': w.employee, 'timestamp': w.created_at})
    recent_activities.sort(key=lambda x: x['timestamp'], reverse=True)

    context = {
        'total_employees': total_employees,
        'active_employees': active_employees,
        'pending_attendance': pending_attendance,
        'total_withdrawals': total_withdrawals,
        'total_payroll': total_payroll,
        'recent_activities': recent_activities[:5],
        'pending_attendances': Attendance.objects.filter(status='pending')[:5],
    }
    return render(request, 'html/admin-dashboard.html', context)


@user_passes_test(is_admin)
@login_required
def manage_employees(request):
    employees = User.objects.filter(is_employee=True).select_related('employee_profile')
    return render(request, 'html/manage-employees.html', {'employees': employees})


@user_passes_test(is_admin)
@login_required
def admin_attendance(request):
    attendances = Attendance.objects.all().select_related('employee').order_by('-date')
    context = {
        'attendances': attendances,
        'pending_count':  attendances.filter(status='pending').count(),
        'approved_count': attendances.filter(status='approved').count(),
        'rejected_count': attendances.filter(status='rejected').count(),
    }
    return render(request, 'html/admin-attendance.html', context)


@user_passes_test(is_admin)
@login_required
def payroll_view(request):
    payroll_data = []
    for employee in User.objects.filter(is_employee=True).select_related('employee_profile'):
        total_earned    = Earning.objects.filter(employee=employee).aggregate(total=Sum('day_pay'))['total'] or 0
        total_withdrawn = Withdrawal.objects.filter(employee=employee, status='completed').aggregate(total=Sum('amount'))['total'] or 0
        balance = total_earned - total_withdrawn
        from django.db.models import Sum as _Sum
        ot_payment = Earning.objects.filter(employee=employee).aggregate(
            total=_Sum('overtime_rate'))['total'] or 0
        payroll_data.append({
            'employee': employee,
            'total_earned': total_earned,
            'total_withdrawn': total_withdrawn,
            'balance': balance,
            'ot_payment': ot_payment,
            'status': 'active' if balance > 0 else 'inactive'
        })

    context = {
        'payroll_data': payroll_data,
        'total_payroll':   sum(i['total_earned']    for i in payroll_data),
        'total_withdrawn': sum(i['total_withdrawn'] for i in payroll_data),
        'total_balance':   sum(i['balance']         for i in payroll_data),
    }
    return render(request, 'html/payroll.html', context)


@user_passes_test(is_admin)
@login_required
def audit_logs(request):
    audit_logs = AuditLog.objects.all().select_related('user').order_by('-timestamp')
    return render(request, 'html/audit-logs.html', {'audit_logs': audit_logs})


@user_passes_test(is_admin)
@login_required
def support_inbox(request):
    tickets = SupportTicket.objects.all().select_related('employee').order_by('-created_at')
    return render(request, 'html/support-inbox.html', {'tickets': tickets})


# ── User Views ────────────────────────────────────────────────────────────────
@login_required
def user_dashboard(request):
    user = request.user
    days_worked   = Attendance.objects.filter(employee=user, status='approved').count()
    total_earned  = Earning.objects.filter(employee=user).aggregate(total=Sum('day_pay'))['total'] or 0
    withdrawals   = Withdrawal.objects.filter(employee=user, status='completed').aggregate(total=Sum('amount'))['total'] or 0
    balance       = total_earned - withdrawals

    context = {
        'days_worked':        days_worked,
        'daily_rate':         getattr(user.employee_profile, 'daily_rate', 0) if hasattr(user, 'employee_profile') else 0,
        'total_earned':       total_earned,
        'balance':            balance,
        'available_balance':  balance,
        'recent_attendances': Attendance.objects.filter(employee=user).order_by('-date')[:3],
        'recent_withdrawals': Withdrawal.objects.filter(employee=user).order_by('-created_at')[:2],
    }
    return render(request, 'html/user-dashboard.html', context)


@login_required
def user_attendance_view(request):
    user  = request.user
    today = timezone.now().date()

    today_attendance = Attendance.objects.filter(employee=user, date=today).first()
    attendance_history = Attendance.objects.filter(employee=user).order_by('-date')[:30]

    context = {
        'current_date':     today,
        'current_time':     timezone.now(),
        'today_attendance': today_attendance,
        'attendance_history': attendance_history,
        'pending_count':    Attendance.objects.filter(employee=user, status='pending').count(),
        'approved_count':   Attendance.objects.filter(employee=user, status='approved').count(),
        'rejected_count':   Attendance.objects.filter(employee=user, status='rejected').count(),
    }
    return render(request, 'html/userattendance.html', context)


@login_required
def user_earnings_view(request):
    user        = request.user
    daily_rate  = getattr(user.employee_profile, 'daily_rate', 1500) if hasattr(user, 'employee_profile') else 1500
    total_earned    = Earning.objects.filter(employee=user).aggregate(total=Sum('day_pay'))['total'] or 0
    total_withdrawn = Withdrawal.objects.filter(employee=user, status='completed').aggregate(total=Sum('amount'))['total'] or 0

    context = {
        'days_worked':       Attendance.objects.filter(employee=user, status='approved').count(),
        'daily_rate':        daily_rate,
        'total_earned':      total_earned,
        'total_withdrawn':   total_withdrawn,
        'available_balance': total_earned - total_withdrawn,
        'approved_earnings': Earning.objects.filter(employee=user).select_related('attendance').order_by('-date'),
    }
    return render(request, 'html/userearning.html', context)


@login_required
def user_withdraw_view(request):
    user            = request.user
    total_earned    = Earning.objects.filter(employee=user).aggregate(total=Sum('day_pay'))['total'] or 0
    total_withdrawn = Withdrawal.objects.filter(employee=user, status='completed').aggregate(total=Sum('amount'))['total'] or 0
    available_balance = total_earned - total_withdrawn
    withdrawal_history = Withdrawal.objects.filter(employee=user).order_by('-created_at')

    if request.method == 'POST':
        form = WithdrawalForm(request.POST)
        if form.is_valid():
            withdrawal = form.save(commit=False)
            withdrawal.employee     = user
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
    if request.method == 'POST':
        form = SupportTicketForm(request.POST)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.employee = request.user
            ticket.save()
            messages.success(request, 'Support ticket submitted successfully!')
            return redirect('contact_admin')
    else:
        form = SupportTicketForm()
    return render(request, 'html/contactadmin.html', {'form': form})


# ── AJAX Views ────────────────────────────────────────────────────────────────

@login_required
def mark_attendance_ajax(request):
    """AJAX endpoint for marking attendance"""
    print(f"mark_attendance_ajax called - Method: {request.method}, User: {request.user.username}")
    
    if request.method == 'POST':
        try:
            user = request.user
            today = timezone.now().date()
            
            print(f"Checking attendance for user {user.username} on {today}")
            
            # Check if already marked
            existing = Attendance.objects.filter(employee=user, date=today).first()
            if existing:
                print(f"Attendance already exists: {existing.id}")
                return JsonResponse({'status': 'error', 'message': 'Attendance already marked for today'})
            
            print(f"Creating new attendance record for {user.username}")
            # Create attendance record
            attendance = Attendance.objects.create(
                employee=user,
                date=today,
                check_in=timezone.now(),
                status='pending'
            )
            
            print(f"Attendance created successfully: {attendance.id}")
            
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
                action='Mark Attendance',
                details=f'Marked attendance for {today}',
                content_type='attendance',
                object_id=str(attendance.id),
                ip_address=request.META.get('REMOTE_ADDR'),
                user_agent=request.META.get('HTTP_USER_AGENT', '')
            )
            
            # Send email notification to admin
            try:
                from main.email_utils import send_attendance_notification
                send_attendance_notification(attendance)
                print(f"Email notification sent for attendance {attendance.id}")
            except Exception as e:
                print(f"Failed to send email notification: {str(e)}")
            
            print(f"Returning success response")
            return JsonResponse({'status': 'success', 'message': 'Attendance marked successfully'})
            
        except Exception as e:
            print(f"Error in mark_attendance_ajax: {str(e)}")
            import traceback
            traceback.print_exc()
            return JsonResponse({'status': 'error', 'message': f'Server error: {str(e)}'})
    
    print(f"Invalid request method: {request.method}")
    return JsonResponse({'status': 'error', 'message': 'Invalid request'})


@login_required
def approve_attendance_ajax(request):
    """Admin approves an attendance record and calculates earnings."""
    if request.method != 'POST':
        return JsonResponse({'status': 'error', 'message': 'Invalid request'})

    if not request.user.is_admin:
        return JsonResponse({'status': 'error', 'message': 'Unauthorized'})

    # ✅ FIX: read from JSON body, not form-encoded POST
    data = _parse_json_body(request)
    attendance_id = data.get('attendance_id') or request.POST.get('attendance_id')

    if not attendance_id:
        return JsonResponse({'status': 'error', 'message': 'attendance_id is required'})

    try:
        attendance = Attendance.objects.get(id=attendance_id)

        if attendance.status != 'pending':
            return JsonResponse({'status': 'error', 'message': 'Attendance already processed'})

        daily_rate   = getattr(attendance.employee.employee_profile, 'daily_rate', 1500) if hasattr(attendance.employee, 'employee_profile') else 1500
        hourly_rate  = daily_rate / 8
        overtime_rate = hourly_rate * 1.5

        if attendance.check_in and attendance.check_out:
            total_seconds  = (attendance.check_out - attendance.check_in).total_seconds()
            work_hours     = total_seconds / 3600
            regular_hours  = min(work_hours, 8)
            overtime_hours = max(work_hours - 8, 0)
            regular_pay    = regular_hours  * hourly_rate
            overtime_pay   = overtime_hours * overtime_rate
            total_pay      = regular_pay + overtime_pay
        else:
            # No check-out recorded — credit a full standard day
            work_hours = regular_hours = 8.0
            overtime_hours = overtime_pay = 0.0
            regular_pay = total_pay = daily_rate

        attendance.overtime_hours = overtime_hours
        attendance.status = 'approved'
        attendance.save()

        Earning.objects.update_or_create(
            attendance=attendance,
            employee=attendance.employee,
            date=attendance.date,
            defaults={
                'daily_rate':     daily_rate,
                'overtime_hours': overtime_hours,
                'overtime_rate':  overtime_rate,
                'day_pay':        total_pay,
            }
        )

        # Send email notification to employee
        try:
            from main.email_utils import send_attendance_approval_notification
            send_attendance_approval_notification(attendance, request.user)
            print(f"Approval notification sent to {attendance.employee.username}")
        except Exception as e:
            print(f"Failed to send approval notification: {str(e)}")

        return JsonResponse({
            'status': 'success',
            'message': 'Attendance approved successfully',
            'data': {
                'work_hours':     round(work_hours, 2),
                'regular_hours':  round(regular_hours, 2),
                'overtime_hours': round(overtime_hours, 2),
                'regular_pay':    round(regular_pay, 2),
                'overtime_pay':   round(overtime_pay, 2),
                'total_pay':      round(total_pay, 2),
            }
        })

    except Attendance.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Attendance not found'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})


@login_required
def reject_attendance_ajax(request):
    """Admin rejects an attendance record."""
    if request.method != 'POST':
        return JsonResponse({'status': 'error', 'message': 'Invalid request'})

    if not request.user.is_admin:
        return JsonResponse({'status': 'error', 'message': 'Unauthorized'})

    # ✅ FIX: read from JSON body, not form-encoded POST
    data = _parse_json_body(request)
    attendance_id = data.get('attendance_id') or request.POST.get('attendance_id')

    if not attendance_id:
        return JsonResponse({'status': 'error', 'message': 'attendance_id is required'})

    try:
        attendance = Attendance.objects.get(id=attendance_id)

        if attendance.status != 'pending':
            return JsonResponse({'status': 'error', 'message': 'Attendance already processed'})

        attendance.status = 'rejected'
        attendance.save()

        # Send email notification to employee
        reason = data.get('reason', 'No reason provided')
        try:
            from main.email_utils import send_attendance_rejection_notification
            send_attendance_rejection_notification(attendance, request.user, reason)
            print(f"Rejection notification sent to {attendance.employee.username}")
        except Exception as e:
            print(f"Failed to send rejection notification: {str(e)}")

        return JsonResponse({'status': 'success', 'message': 'Attendance rejected successfully'})

    except Attendance.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Attendance not found'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})


@login_required
def process_withdrawal_ajax(request):
    if request.method != 'POST':
        return JsonResponse({'status': 'error', 'message': 'Invalid request'})

    user   = request.user
    data   = _parse_json_body(request)
    amount = data.get('amount') or request.POST.get('amount')

    total_earned    = Earning.objects.filter(employee=user).aggregate(total=Sum('day_pay'))['total'] or 0
    total_withdrawn = Withdrawal.objects.filter(employee=user, status='completed').aggregate(total=Sum('amount'))['total'] or 0
    available_balance = total_earned - total_withdrawn

    if float(amount) > available_balance:
        return JsonResponse({'status': 'error', 'message': 'Insufficient balance'})

    withdrawal = Withdrawal.objects.create(
        employee=user,
        amount=amount,
        phone_number=user.phone_number,
        status='pending'
    )
    AuditLog.objects.create(
        user=user, action='create', model_name='Withdrawal',
        object_id=withdrawal.id, object_repr=str(withdrawal),
        ip_address=request.META.get('REMOTE_ADDR'),
        user_agent=request.META.get('HTTP_USER_AGENT', '')
    )
    return JsonResponse({'status': 'success', 'message': 'Withdrawal request submitted'})


@csrf_exempt
@login_required
def user_attendance_history_ajax(request):
    if request.method != 'GET':
        return JsonResponse({'status': 'error', 'message': 'Invalid request'})

    attendances = Attendance.objects.filter(employee=request.user).order_by('-date').values(
        'date', 'check_in', 'check_out', 'status'
    )
    serialized = [{
        'date':      a['date'].isoformat()      if a['date']      else None,
        'check_in':  a['check_in'].isoformat()  if a['check_in']  else None,
        'check_out': a['check_out'].isoformat() if a['check_out'] else None,
        'status':    a['status'],
    } for a in attendances]

    return JsonResponse({'status': 'success', 'data': serialized})


@csrf_exempt
@login_required
def user_withdrawal_history_ajax(request):
    if request.method != 'GET':
        return JsonResponse({'status': 'error', 'message': 'Invalid request'})

    withdrawals = Withdrawal.objects.filter(employee=request.user).order_by('-created_at').values(
        'id', 'amount', 'status', 'created_at'
    )
    return JsonResponse({'status': 'success', 'data': list(withdrawals)})


@csrf_exempt
@login_required
def withdrawal_status_ajax(request, withdrawal_id):
    if request.method != 'GET':
        return JsonResponse({'status': 'error', 'message': 'Invalid request'})

    try:
        w = Withdrawal.objects.get(id=withdrawal_id, employee=request.user)
        return JsonResponse({'status': 'success', 'data': {'id': w.id, 'status': w.status, 'amount': float(w.amount)}})
    except Withdrawal.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Withdrawal not found'})


@csrf_exempt
@login_required
def withdrawal_updates_ajax(request):
    if request.method != 'GET':
        return JsonResponse({'status': 'error', 'message': 'Invalid request'})

    recent = Withdrawal.objects.filter(
        employee=request.user, status__in=['pending', 'processing']
    ).order_by('-created_at')[:5]

    return JsonResponse({'status': 'success', 'has_updates': recent.exists(), 'data': list(recent.values())})