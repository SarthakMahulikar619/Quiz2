from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Count, Avg, Q, Sum
from django.utils import timezone
from datetime import datetime, timedelta
from django.db import models

from .models import (
    Department, Position, Employee, Attendance
)
from .serializers import (
    DepartmentSerializer, PositionSerializer, EmployeeSerializer, 
    EmployeeListSerializer, AttendanceSerializer, EmployeeAnalyticsSerializer,
    AttendanceAnalyticsSerializer
)


class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'created_at']
    ordering = ['name']

    @action(detail=True, methods=['get'])
    def employees(self, request, pk=None):
        """Get all employees in a department"""
        department = self.get_object()
        employees = Employee.objects.filter(position__department=department)
        serializer = EmployeeListSerializer(employees, many=True)
        return Response(serializer.data)


class PositionViewSet(viewsets.ModelViewSet):
    queryset = Position.objects.select_related('department')
    serializer_class = PositionSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['department', 'level']
    search_fields = ['title', 'description']
    ordering_fields = ['title', 'base_salary']
    ordering = ['title']

    @action(detail=True, methods=['get'])
    def employees(self, request, pk=None):
        """Get all employees in a position"""
        position = self.get_object()
        employees = position.employees.all()
        serializer = EmployeeListSerializer(employees, many=True)
        return Response(serializer.data)


class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.select_related('position__department')
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['position', 'position__department', 'is_active', 'gender', 'marital_status']
    search_fields = ['first_name', 'last_name', 'email', 'employee_id']
    ordering_fields = ['first_name', 'last_name', 'hire_date', 'salary']
    ordering = ['last_name', 'first_name']

    def get_serializer_class(self):
        if self.action == 'list':
            return EmployeeListSerializer
        return EmployeeSerializer

    @action(detail=True, methods=['get'])
    def attendance(self, request, pk=None):
        """Get attendance records for an employee"""
        employee = self.get_object()
        attendance = employee.attendances.all()
        serializer = AttendanceSerializer(attendance, many=True)
        return Response(serializer.data)



    @action(detail=False, methods=['get'])
    def analytics(self, request):
        """Get employee analytics summary"""
        total_employees = Employee.objects.count()
        active_employees = Employee.objects.filter(is_active=True).count()
        
        # Employees by department
        employees_by_department = Employee.objects.values(
            'position__department__name'
        ).annotate(
            count=Count('id')
        ).order_by('-count')
        
        # Employees by position
        employees_by_position = Employee.objects.values(
            'position__title'
        ).annotate(
            count=Count('id')
        ).order_by('-count')
        
        # Average salary
        avg_salary = Employee.objects.aggregate(
            avg_salary=Avg('salary')
        )['avg_salary'] or 0
        
        # New hires this month
        current_month = timezone.now().replace(day=1)
        new_hires_this_month = Employee.objects.filter(
            hire_date__gte=current_month
        ).count()
        
        analytics_data = {
            'total_employees': total_employees,
            'active_employees': active_employees,
            'employees_by_department': {item['position__department__name']: item['count'] 
                                      for item in employees_by_department},
            'employees_by_position': {item['position__title']: item['count'] 
                                    for item in employees_by_position},
            'average_salary': avg_salary,
            'new_hires_this_month': new_hires_this_month
        }
        
        serializer = EmployeeAnalyticsSerializer(analytics_data)
        return Response(serializer.data)


class AttendanceViewSet(viewsets.ModelViewSet):
    queryset = Attendance.objects.select_related('employee')
    serializer_class = AttendanceSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['employee', 'status', 'date']
    search_fields = ['employee__first_name', 'employee__last_name', 'employee__employee_id']
    ordering_fields = ['date', 'hours_worked']
    ordering = ['-date']

    @action(detail=False, methods=['get'])
    def analytics(self, request):
        """Get attendance analytics summary"""
        total_records = Attendance.objects.count()
        
        # Attendance rate (present vs total)
        present_count = Attendance.objects.filter(status='present').count()
        attendance_rate = (present_count / total_records * 100) if total_records > 0 else 0
        
        # Average hours worked
        avg_hours = Attendance.objects.aggregate(
            avg_hours=Avg('hours_worked')
        )['avg_hours'] or 0
        
        # Attendance by status
        attendance_by_status = Attendance.objects.values('status').annotate(
            count=Count('id')
        ).order_by('-count')
        
        # Top attending employees
        top_attending = Attendance.objects.values(
            'employee__first_name', 'employee__last_name', 'employee__employee_id'
        ).annotate(
            total_hours=Sum('hours_worked'),
            attendance_count=Count('id')
        ).order_by('-total_hours')[:10]
        
        analytics_data = {
            'total_attendance_records': total_records,
            'attendance_rate': attendance_rate,
            'average_hours_worked': avg_hours,
            'attendance_by_status': {item['status']: item['count'] 
                                   for item in attendance_by_status},
            'top_attending_employees': [
                {
                    'name': f"{item['employee__first_name']} {item['employee__last_name']}",
                    'employee_id': item['employee__employee_id'],
                    'total_hours': item['total_hours'],
                    'attendance_count': item['attendance_count']
                }
                for item in top_attending
            ]
        }
        
        serializer = AttendanceAnalyticsSerializer(analytics_data)
        return Response(serializer.data)






# Health check endpoint
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render

@csrf_exempt
def health_check(request):
    """Health check endpoint"""
    return JsonResponse({
        'status': 'healthy',
        'timestamp': timezone.now().isoformat(),
        'version': '1.0.0'
    })

def dashboard(request):
    """Dashboard view with visualizations"""
    return render(request, 'employees/dashboard.html')