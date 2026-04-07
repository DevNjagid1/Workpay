from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate
from .models import User, Employee, Attendance, Withdrawal, SupportTicket

class CustomUserCreationForm(UserCreationForm):
    """Registration form with additional fields"""
    first_name = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'First name'
        })
    )
    last_name = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Last name'
        })
    )
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'name@email.com'
        })
    )
    phone_number = forms.CharField(
        max_length=20,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '+254XXXXXXXXX'
        })
    )
    employee_id = forms.CharField(
        max_length=20,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'EMP001'
        })
    )

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'phone_number', 'employee_id', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_employee = True  # Set user as employee by default
        user.is_admin = False   # Ensure they're not admin
        if commit:
            user.save()
        return user

class LoginForm(forms.Form):
    """Login form with username and password"""
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Username or Employee ID'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Password',
            'id': 'password'
        })
    )

class EmployeeForm(forms.ModelForm):
    """Form for creating/updating employees"""
    class Meta:
        model = Employee
        fields = ['start_date', 'status', 'department', 'position']
        widgets = {
            'start_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'department': forms.TextInput(attrs={'class': 'form-control'}),
            'position': forms.TextInput(attrs={'class': 'form-control'}),
        }

class AttendanceForm(forms.ModelForm):
    """Form for attendance records"""
    class Meta:
        model = Attendance
        fields = ['date', 'check_in', 'check_out', 'status', 'overtime_hours']
        widgets = {
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'check_in': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'check_out': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'overtime_hours': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.5', 'min': '0'}),
        }

class WithdrawalForm(forms.ModelForm):
    """Form for withdrawal requests"""
    class Meta:
        model = Withdrawal
        fields = ['amount', 'notes']
        widgets = {
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'step': '50', 'min': '50'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Optional notes...'}),
        }

class SupportTicketForm(forms.ModelForm):
    """Form for support tickets"""
    class Meta:
        model = SupportTicket
        fields = ['category', 'subject', 'message', 'priority']
        widgets = {
            'category': forms.Select(attrs={'class': 'form-control'}),
            'subject': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Subject'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Describe your issue...'}),
            'priority': forms.Select(attrs={'class': 'form-control'}),
        }

class EmployeeBulkCreateForm(forms.Form):
    """Form for bulk creating employees"""
    file = forms.FileField(
        widget=forms.FileInput(attrs={'class': 'form-control', 'accept': '.csv,.xlsx'})
    )

class AttendanceApprovalForm(forms.ModelForm):
    """Form for approving/rejecting attendance"""
    class Meta:
        model = Attendance
        fields = ['status', 'notes']
        widgets = {
            'status': forms.Select(attrs={'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Optional notes...'}),
        }

class WithdrawalProcessForm(forms.ModelForm):
    """Form for processing withdrawals"""
    class Meta:
        model = Withdrawal
        fields = ['status', 'receipt_number', 'mpesa_transaction_id', 'notes']
        widgets = {
            'status': forms.Select(attrs={'class': 'form-control'}),
            'receipt_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'M-Pesa receipt number'}),
            'mpesa_transaction_id': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Transaction ID'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Processing notes...'}),
        }

class SupportTicketResponseForm(forms.ModelForm):
    """Form for responding to support tickets"""
    class Meta:
        model = SupportTicket
        fields = ['status', 'admin_response']
        widgets = {
            'status': forms.Select(attrs={'class': 'form-control'}),
            'admin_response': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Response to employee'
            }),
        }

class UserProfileForm(forms.ModelForm):
    """Form for users to update their profile"""
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'phone_number']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
        }

class PasswordChangeForm(forms.Form):
    """Form for changing password"""
    current_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Current password'
        })
    )
    new_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'New password'
        })
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirm new password'
        })
    )

    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get('new_password')
        confirm_password = cleaned_data.get('confirm_password')
        
        if new_password and confirm_password and new_password != confirm_password:
            raise forms.ValidationError('New passwords do not match')
        
        return cleaned_data
