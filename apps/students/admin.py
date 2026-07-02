from django.contrib import admin

from .models import Student, StudentEnrollment


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'school', 'student_code', 'status', 'is_active']
    list_filter = ['status', 'is_active', 'tenant']
    search_fields = ['full_name', 'preferred_name', 'document_number', 'student_code', 'email', 'school__name']
    autocomplete_fields = ['tenant', 'school']


@admin.register(StudentEnrollment)
class StudentEnrollmentAdmin(admin.ModelAdmin):
    list_display = ['student', 'school', 'academic_year', 'class_group', 'status', 'enrolled_at']
    list_filter = ['status', 'tenant', 'academic_year']
    search_fields = ['student__full_name', 'enrollment_number', 'school__name', 'class_group__name']
    autocomplete_fields = ['tenant', 'student', 'school', 'academic_year', 'class_group']
