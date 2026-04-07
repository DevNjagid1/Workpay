from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from decimal import Decimal
from datetime import date, timedelta, datetime
import random

User = get_user_model()

class Command(BaseCommand):
    help = 'Seed the database with initial data for testing'

    def handle(self, *args, **options):
        self.stdout.write('🌱 Seeding database with initial data...')
        
        # Create admin user
        if not User.objects.filter(username='admin').exists():
            admin_user = User.objects.create_user(
                username='admin',
                email='admin@kazisafi.co.ke',
                password='admin123',
                first_name='System',
                last_name='Administrator',
                phone_number='+254700100000',
                employee_id='ADMIN001',
                daily_rate=Decimal('0.00'),
                is_admin=True,
                is_employee=False
            )
            self.stdout.write(f"✅ Created admin user: {admin_user.username}")
        
        # Create test employees
        employees_data = [
            {
                'username': 'jwanjiku',
                'email': 'jane.wanjiku@kazisafi.co.ke',
                'password': 'password123',
                'first_name': 'Jane',
                'last_name': 'Wanjiku',
                'phone_number': '+254700100001',
                'employee_id': 'EMP001',
                'daily_rate': Decimal('1500.00'),
                'start_date': '2024-01-15',
                'department': 'Operations',
                'position': 'General Worker'
            },
            {
                'username': 'pomondi',
                'email': 'peter.omondi@kazisafi.co.ke',
                'password': 'password123',
                'first_name': 'Peter',
                'last_name': 'Omondi',
                'phone_number': '+254700100002',
                'employee_id': 'EMP002',
                'daily_rate': Decimal('1500.00'),
                'start_date': '2024-02-01',
                'department': 'Operations',
                'position': 'General Worker'
            },
            {
                'username': 'makinyi',
                'email': 'mary.akinyi@kazisafi.co.ke',
                'password': 'password123',
                'first_name': 'Mary',
                'last_name': 'Akinyi',
                'phone_number': '+254700100003',
                'employee_id': 'EMP003',
                'daily_rate': Decimal('1800.00'),
                'start_date': '2024-01-09',
                'department': 'Operations',
                'position': 'Senior Worker'
            },
            {
                'username': 'skamau',
                'email': 'samuel.kamau@kazisafi.co.ke',
                'password': 'password123',
                'first_name': 'Samuel',
                'last_name': 'Kamau',
                'phone_number': '+254700100004',
                'employee_id': 'EMP004',
                'daily_rate': Decimal('1200.00'),
                'start_date': '2024-03-12',
                'department': 'Operations',
                'position': 'General Worker'
            },
            {
                'username': 'cmutua',
                'email': 'catherine.mutua@kazisafi.co.ke',
                'password': 'password123',
                'first_name': 'Catherine',
                'last_name': 'Mutua',
                'phone_number': '+254700100005',
                'employee_id': 'EMP005',
                'daily_rate': Decimal('2000.00'),
                'start_date': '2024-05-20',
                'department': 'Operations',
                'position': 'Team Lead'
            }
        ]
        
        employees = []
        for emp_data in employees_data:
            if not User.objects.filter(username=emp_data['username']).exists():
                user = User.objects.create_user(
                    username=emp_data['username'],
                    email=emp_data['email'],
                    password=emp_data['password'],
                    first_name=emp_data['first_name'],
                    last_name=emp_data['last_name'],
                    phone_number=emp_data['phone_number'],
                    employee_id=emp_data['employee_id'],
                    daily_rate=emp_data['daily_rate'],
                    is_admin=False,
                    is_employee=True
                )
                
                # Create employee profile
                from main.models import Employee
                Employee.objects.create(
                    user=user,
                    start_date=emp_data['start_date'],
                    status='active',
                    department=emp_data['department'],
                    position=emp_data['position']
                )
                
                self.stdout.write(f"✅ Created employee: {emp_data['first_name']} {emp_data['last_name']}")
                employees.append(user)
            else:
                employees.append(User.objects.get(username=emp_data['username']))
        
        # Create sample attendance records
        from main.models import Attendance, Earning
        
        today = date.today()
        
        for i in range(30):  # Create 30 days of attendance
            attendance_date = today - timedelta(days=i)
            
            for employee in employees:
                # Check if attendance already exists for this employee and date
                if Attendance.objects.filter(employee=employee, date=attendance_date).exists():
                    continue
                    
                # Random status for variety
                status = random.choice(['approved', 'approved', 'approved', 'pending', 'rejected'])
                
                attendance = Attendance.objects.create(
                    employee=employee,
                    date=attendance_date,
                    check_in=datetime.combine(attendance_date, datetime.min.time().replace(hour=8, minute=random.randint(0, 30))),
                    status=status,
                    overtime_hours=random.choice([0, 0, 0, 1, 2, 0.5, 1.5])
                )
                
                # Create corresponding earning if approved
                if status == 'approved':
                    daily_rate = employee.daily_rate
                    overtime_hours = Decimal(str(attendance.overtime_hours))
                    overtime_pay = overtime_hours * (daily_rate * Decimal('1.5') / Decimal('8'))  # 1.5x rate for overtime
                    day_pay = daily_rate + overtime_pay
                    
                    Earning.objects.create(
                        employee=employee,
                        attendance=attendance,
                        date=attendance_date,
                        daily_rate=daily_rate,
                        overtime_hours=attendance.overtime_hours,
                        overtime_rate=daily_rate * Decimal('1.5') / Decimal('8'),
                        day_pay=day_pay
                    )
        
        self.stdout.write("✅ Created sample attendance and earnings data")
        
        # Create sample withdrawal records
        from main.models import Withdrawal
        withdrawal_data = [
            {
                'employee': employees[0],  # Jane Wanjiku
                'amount': Decimal('1000.00'),
                'status': 'completed',
                'receipt_number': 'MP123456789',
                'mpesa_transaction_id': 'TXN987654321',
                'notes': 'Monthly withdrawal'
            },
            {
                'employee': employees[1],  # Peter Omondi
                'amount': Decimal('1500.00'),
                'status': 'completed',
                'receipt_number': 'MP123456790',
                'mpesa_transaction_id': 'TXN987654322',
                'notes': 'Emergency withdrawal'
            },
            {
                'employee': employees[2],  # Mary Akinyi
                'amount': Decimal('2000.00'),
                'status': 'pending',
                'notes': 'Pending withdrawal'
            }
        ]
        
        for withdrawal in withdrawal_data:
            Withdrawal.objects.create(**withdrawal)
        
        self.stdout.write("✅ Created sample withdrawal data")
        
        # Create sample support tickets
        from main.models import SupportTicket
        ticket_data = [
            {
                'employee': employees[0],
                'subject': 'Request for salary advance',
                'message': 'I would like to request a salary advance for emergency medical expenses. Please advise on the process and timeline.',
                'priority': 'high',
                'status': 'open'
            },
            {
                'employee': employees[1],
                'subject': 'Issue with attendance system',
                'message': 'The attendance system is not recognizing my check-ins for the past 3 days. I have been on time but the system shows me as absent.',
                'priority': 'medium',
                'status': 'in_progress'
            },
            {
                'employee': employees[2],
                'subject': 'Question about overtime calculation',
                'message': 'Could you please clarify how overtime is calculated? I worked 2 extra hours on Saturday but my pay seems incorrect.',
                'priority': 'low',
                'status': 'resolved',
                'admin_response': 'Overtime is calculated at 1.5x your hourly rate. Your Saturday hours have been adjusted in your latest payment.'
            }
        ]
        
        for ticket in ticket_data:
            SupportTicket.objects.create(**ticket)
        
        self.stdout.write("✅ Created sample support tickets")
        
        # Create audit logs
        from main.models import AuditLog
        audit_data = [
            {
                'user': User.objects.get(username='admin'),
                'action': 'login',
                'model_name': 'User',
                'object_id': 1,
                'object_repr': 'System Administrator',
                'ip_address': '127.0.0.1',
                'user_agent': 'Mozilla/5.0 (Django Seeder)'
            },
            {
                'user': employees[0],
                'action': 'create',
                'model_name': 'Attendance',
                'object_id': 1,
                'object_repr': 'Jane Wanjiku - 2024-02-01 (approved)',
                'ip_address': '192.168.1.100'
            }
        ]
        
        for audit in audit_data:
            AuditLog.objects.create(**audit)
        
        self.stdout.write("✅ Created sample audit logs")
        
        # Summary
        self.stdout.write(self.style.SUCCESS("🎉 Database seeding completed successfully!"))
        self.stdout.write(f"📊 Created {User.objects.count()} users")
        from main.models import Employee
        self.stdout.write(f"👥 Created {Employee.objects.count()} employee profiles")
        from main.models import Attendance
        self.stdout.write(f"⏰ Created {Attendance.objects.count()} attendance records")
        from main.models import Earning
        self.stdout.write(f"💰 Created {Earning.objects.count()} earning records")
        from main.models import Withdrawal
        self.stdout.write(f"💸 Created {Withdrawal.objects.count()} withdrawal records")
        from main.models import SupportTicket
        self.stdout.write(f"🎫 Created {SupportTicket.objects.count()} support tickets")
        from main.models import AuditLog
        self.stdout.write(f"📋 Created {AuditLog.objects.count()} audit logs")
