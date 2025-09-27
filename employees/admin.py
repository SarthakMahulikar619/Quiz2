from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe

from .models import (
    Department, Position, Employee, Attendance
)


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['name', 'budget', 'employee_count', 'created_at']
    list_filter = ['created_at']
    search_fields = ['name', 'description']
    readonly_fields = ['created_at', 'updated_at']
    
    def employee_count(self, obj):
        count = sum(pos.employees.count() for pos in obj.positions.all())
        return count
    employee_count.short_description = 'Employees'


@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    list_display = ['title', 'department', 'level', 'base_salary', 'employee_count']
    list_filter = ['department', 'level']
    search_fields = ['title', 'description']
    readonly_fields = ['created_at']
    
    def employee_count(self, obj):
        return obj.employees.count()
    employee_count.short_description = 'Employees'


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = [
        'employee_id', 'full_name', 'position', 'department', 
        'hire_date', 'salary', 'is_active', 'status_color'
    ]
    list_filter = [
        'position__department', 'position', 'is_active', 
        'gender', 'marital_status', 'hire_date'
    ]
    search_fields = [
        'first_name', 'last_name', 'email', 'employee_id', 
        'phone', 'position__title'
    ]
    readonly_fields = ['employee_id', 'created_at', 'updated_at']
    fieldsets = (
        ('Basic Information', {
            'fields': ('employee_id', 'first_name', 'last_name', 'email', 'phone')
        }),
        ('Personal Details', {
            'fields': ('date_of_birth', 'gender', 'marital_status')
        }),
        ('Address', {
            'fields': ('address', 'city', 'state', 'postal_code', 'country')
        }),
        ('Employment', {
            'fields': ('position', 'hire_date', 'salary', 'is_active')
        }),
        ('Emergency Contact', {
            'fields': ('emergency_contact_name', 'emergency_contact_phone', 'emergency_contact_relationship')
        }),
        ('System', {
            'fields': ('created_by', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def department(self, obj):
        return obj.position.department.name
    department.short_description = 'Department'
    
    def status_color(self, obj):
        if obj.is_active:
            return format_html('<span style="color: green;">Active</span>')
        return format_html('<span style="color: red;">Inactive</span>')
    status_color.short_description = 'Status'


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = [
        'employee', 'date', 'check_in_time', 'check_out_time', 
        'hours_worked', 'status', 'status_color'
    ]
    list_filter = ['status', 'date', 'employee__position__department']
    search_fields = [
        'employee__first_name', 'employee__last_name', 
        'employee__employee_id'
    ]
    readonly_fields = ['created_at']
    date_hierarchy = 'date'
    
    def status_color(self, obj):
        colors = {
            'present': 'green',
            'absent': 'red',
            'late': 'orange',
            'sick_leave': 'blue',
            'vacation': 'purple',
            'half_day': 'yellow'
        }
        color = colors.get(obj.status, 'black')
        return format_html('<span style="color: {};">{}</span>', color, obj.status.title())
    status_color.short_description = 'Status'






# Customize admin site
admin.site.site_header = "Employee Data Management System"
admin.site.site_title = "Employee Admin"
admin.site.index_title = "Welcome to Employee Data Management"