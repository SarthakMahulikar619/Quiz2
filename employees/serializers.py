from rest_framework import serializers
from django.contrib.auth.models import User
from django.db import models
from .models import (
    Department, Position, Employee, Attendance
)


class DepartmentSerializer(serializers.ModelSerializer):
    employee_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Department
        fields = '__all__'
    
    def get_employee_count(self, obj):
        return obj.positions.aggregate(
            total=models.Count('employees')
        )['total'] or 0


class PositionSerializer(serializers.ModelSerializer):
    department_name = serializers.CharField(source='department.name', read_only=True)
    employee_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Position
        fields = '__all__'
    
    def get_employee_count(self, obj):
        return obj.employees.count()


class EmployeeSerializer(serializers.ModelSerializer):
    position_title = serializers.CharField(source='position.title', read_only=True)
    department_name = serializers.CharField(source='position.department.name', read_only=True)
    full_name = serializers.CharField(read_only=True)
    
    class Meta:
        model = Employee
        fields = '__all__'
        read_only_fields = ['employee_id', 'created_at', 'updated_at']


class EmployeeListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for employee lists"""
    position_title = serializers.CharField(source='position.title', read_only=True)
    department_name = serializers.CharField(source='position.department.name', read_only=True)
    full_name = serializers.CharField(read_only=True)
    
    class Meta:
        model = Employee
        fields = [
            'id', 'employee_id', 'full_name', 'email', 'phone',
            'position_title', 'department_name', 'hire_date', 
            'salary', 'is_active'
        ]


class AttendanceSerializer(serializers.ModelSerializer):
    employee_name = serializers.CharField(source='employee.full_name', read_only=True)
    employee_id = serializers.CharField(source='employee.employee_id', read_only=True)
    
    class Meta:
        model = Attendance
        fields = '__all__'
        read_only_fields = ['created_at']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'is_staff']


# Analytics Serializers
class EmployeeAnalyticsSerializer(serializers.Serializer):
    total_employees = serializers.IntegerField()
    active_employees = serializers.IntegerField()
    employees_by_department = serializers.DictField()
    employees_by_position = serializers.DictField()
    average_salary = serializers.DecimalField(max_digits=10, decimal_places=2)
    new_hires_this_month = serializers.IntegerField()


class AttendanceAnalyticsSerializer(serializers.Serializer):
    total_attendance_records = serializers.IntegerField()
    attendance_rate = serializers.DecimalField(max_digits=5, decimal_places=2)
    average_hours_worked = serializers.DecimalField(max_digits=4, decimal_places=2)
    attendance_by_status = serializers.DictField()
    top_attending_employees = serializers.ListField()
