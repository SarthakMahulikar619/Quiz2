from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import datetime, timedelta, date, time
import random
from decimal import Decimal

from employees.models import (
    Department, Position, Employee, Attendance
)


class Command(BaseCommand):
    help = 'Generate synthetic employee data for testing and demonstration'

    def add_arguments(self, parser):
        parser.add_argument(
            '--employees',
            type=int,
            default=5,
            help='Number of employees to generate (default: 5)'
        )
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear existing data before generating new data'
        )

    def handle(self, *args, **options):
        if options['clear']:
            self.stdout.write('Clearing existing data...')
            self.clear_data()

        num_employees = options['employees']
        self.stdout.write(f'Generating data for {num_employees} employees...')

        # Create superuser if not exists
        self.create_superuser()

        # Generate departments
        departments = self.create_departments()

        # Generate positions
        positions = self.create_positions(departments)

        # Generate employees
        employees = self.create_employees(positions, num_employees)

        # Generate attendance records
        self.create_attendance_records(employees)


        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully generated data for {num_employees} employees!'
            )
        )

    def clear_data(self):
        """Clear all existing data"""
        Attendance.objects.all().delete()
        Employee.objects.all().delete()
        Position.objects.all().delete()
        Department.objects.all().delete()

    def create_superuser(self):
        """Create superuser if not exists"""
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser(
                username='admin',
                email='admin@example.com',
                password='admin123'
            )
            self.stdout.write('Created superuser: admin/admin123')

    def create_departments(self):
        """Create departments"""
        departments_data = [
            {'name': 'Human Resources', 'description': 'HR and employee management', 'budget': 500000},
            {'name': 'Engineering', 'description': 'Software development and technical operations', 'budget': 2000000},
            {'name': 'Marketing', 'description': 'Marketing and brand management', 'budget': 800000},
            {'name': 'Sales', 'description': 'Sales and customer relations', 'budget': 1200000},
            {'name': 'Finance', 'description': 'Financial management and accounting', 'budget': 600000},
        ]

        departments = []
        for dept_data in departments_data:
            dept, created = Department.objects.get_or_create(
                name=dept_data['name'],
                defaults=dept_data
            )
            departments.append(dept)
            if created:
                self.stdout.write(f'Created department: {dept.name}')

        return departments

    def create_positions(self, departments):
        """Create positions for each department"""
        positions_data = [
            # HR positions
            {'title': 'HR Manager', 'level': 'manager', 'base_salary': 80000},
            {'title': 'HR Specialist', 'level': 'mid', 'base_salary': 55000},
            {'title': 'Recruiter', 'level': 'mid', 'base_salary': 50000},
            
            # Engineering positions
            {'title': 'Engineering Director', 'level': 'director', 'base_salary': 150000},
            {'title': 'Senior Software Engineer', 'level': 'senior', 'base_salary': 120000},
            {'title': 'Software Engineer', 'level': 'mid', 'base_salary': 90000},
            {'title': 'Junior Developer', 'level': 'entry', 'base_salary': 65000},
            {'title': 'DevOps Engineer', 'level': 'senior', 'base_salary': 110000},
            
            # Marketing positions
            {'title': 'Marketing Director', 'level': 'director', 'base_salary': 130000},
            {'title': 'Marketing Manager', 'level': 'manager', 'base_salary': 85000},
            {'title': 'Content Specialist', 'level': 'mid', 'base_salary': 55000},
            {'title': 'Social Media Coordinator', 'level': 'entry', 'base_salary': 45000},
            
            # Sales positions
            {'title': 'Sales Director', 'level': 'director', 'base_salary': 140000},
            {'title': 'Sales Manager', 'level': 'manager', 'base_salary': 90000},
            {'title': 'Sales Representative', 'level': 'mid', 'base_salary': 60000},
            {'title': 'Account Executive', 'level': 'senior', 'base_salary': 75000},
            
            # Finance positions
            {'title': 'CFO', 'level': 'director', 'base_salary': 160000},
            {'title': 'Financial Analyst', 'level': 'mid', 'base_salary': 65000},
            {'title': 'Accountant', 'level': 'mid', 'base_salary': 55000},
        ]

        positions = []
        for pos_data in positions_data:
            # Assign to appropriate department
            dept_name = self.get_department_for_position(pos_data['title'])
            department = next((d for d in departments if d.name == dept_name), departments[0])
            
            pos, created = Position.objects.get_or_create(
                title=pos_data['title'],
                department=department,
                defaults=pos_data
            )
            positions.append(pos)
            if created:
                self.stdout.write(f'Created position: {pos.title} in {pos.department.name}')

        return positions

    def get_department_for_position(self, title):
        """Get department name for a position title"""
        if any(word in title.lower() for word in ['hr', 'human']):
            return 'Human Resources'
        elif any(word in title.lower() for word in ['engineer', 'developer', 'devops', 'software']):
            return 'Engineering'
        elif any(word in title.lower() for word in ['marketing', 'content', 'social']):
            return 'Marketing'
        elif any(word in title.lower() for word in ['sales', 'account']):
            return 'Sales'
        elif any(word in title.lower() for word in ['finance', 'financial', 'accountant', 'cfo']):
            return 'Finance'
        else:
            return 'Human Resources'

    def create_employees(self, positions, num_employees):
        """Create employees"""
        from faker import Faker
        fake = Faker()

        employees = []
        for i in range(num_employees):
            position = random.choice(positions)
            
            # Generate unique employee ID
            while True:
                employee_id = f"EMP{1000 + i + random.randint(0, 9999):04d}"
                if not Employee.objects.filter(employee_id=employee_id).exists():
                    break
            
            # Generate hire date (within last 2 years)
            hire_date = fake.date_between(start_date='-2y', end_date='today')
            
            # Calculate salary based on position with some variation
            base_salary = position.base_salary
            salary_variation = random.uniform(0.8, 1.2)
            salary = Decimal(str(round(float(base_salary) * salary_variation, 2)))

            employee_data = {
                'employee_id': employee_id,
                'first_name': fake.first_name(),
                'last_name': fake.last_name(),
                'email': fake.email(),
                'phone': fake.phone_number()[:15],
                'date_of_birth': fake.date_of_birth(minimum_age=22, maximum_age=65),
                'gender': random.choice(['M', 'F', 'O']),
                'marital_status': random.choice(['single', 'married', 'divorced']),
                'address': fake.street_address(),
                'city': fake.city(),
                'state': fake.state(),
                'postal_code': fake.postcode(),
                'country': 'USA',
                'position': position,
                'hire_date': hire_date,
                'salary': salary,
                'is_active': random.choice([True, True, True, False]),  # 75% active
                'emergency_contact_name': fake.name(),
                'emergency_contact_phone': fake.phone_number()[:15],
                'emergency_contact_relationship': random.choice(['Spouse', 'Parent', 'Sibling', 'Friend']),
            }

            employee = Employee.objects.create(**employee_data)
            employees.append(employee)
            self.stdout.write(f'Created employee: {employee.full_name} ({employee.employee_id})')

        return employees

    def create_attendance_records(self, employees):
        """Create attendance records for employees"""
        from faker import Faker
        fake = Faker()

        for employee in employees:
            # Generate attendance for last 30 days
            for i in range(30):
                attendance_date = timezone.now().date() - timedelta(days=i)
                
                # Skip weekends
                if attendance_date.weekday() >= 5:
                    continue
                
                # 85% attendance rate
                if random.random() < 0.85:
                    status = 'present'
                    check_in = time(9, random.randint(0, 30))  # 9:00-9:30 AM
                    check_out = time(17, random.randint(0, 30))  # 5:00-5:30 PM
                    hours_worked = 8.0
                else:
                    status = random.choice(['absent', 'sick_leave', 'vacation'])
                    check_in = None
                    check_out = None
                    hours_worked = 0

                Attendance.objects.create(
                    employee=employee,
                    date=attendance_date,
                    check_in_time=check_in,
                    check_out_time=check_out,
                    hours_worked=hours_worked,
                    status=status,
                    notes=fake.sentence() if status != 'present' else ''
                )

        self.stdout.write('Created attendance records')

