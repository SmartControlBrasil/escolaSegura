from django.contrib import admin

from .models import AbsenceJustification, AttendanceRecord, AttendanceSession


@admin.register(AttendanceSession)
class AttendanceSessionAdmin(admin.ModelAdmin):
    list_display = ['school', 'class_group', 'subject', 'session_date', 'session_number', 'status', 'teacher']
    list_filter = ['status', 'session_date', 'school', 'class_group']
    search_fields = ['class_group__name', 'subject__name', 'teacher__full_name']
    autocomplete_fields = ['tenant', 'school', 'academic_year', 'class_group', 'subject', 'teacher']


@admin.register(AttendanceRecord)
class AttendanceRecordAdmin(admin.ModelAdmin):
    list_display = ['session', 'student', 'status', 'arrival_time', 'marked_at']
    list_filter = ['status', 'session__session_date', 'session__class_group']
    search_fields = ['student__full_name', 'student__student_code']
    autocomplete_fields = ['tenant', 'session', 'student', 'enrollment', 'marked_by']


@admin.register(AbsenceJustification)
class AbsenceJustificationAdmin(admin.ModelAdmin):
    list_display = ['record', 'status', 'submitted_by', 'reviewed_by', 'reviewed_at', 'created_at']
    list_filter = ['status', 'created_at', 'reviewed_at']
    search_fields = ['record__student__full_name', 'reason', 'review_notes']
    autocomplete_fields = ['tenant', 'record', 'submitted_by', 'reviewed_by']
