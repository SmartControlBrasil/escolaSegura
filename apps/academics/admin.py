from django.contrib import admin

from .models import ClassGroup, GradeLevel, Subject, TeacherAssignment, TeacherProfile


@admin.register(GradeLevel)
class GradeLevelAdmin(admin.ModelAdmin):
    list_display = ['name', 'school', 'stage', 'order', 'is_active']
    list_filter = ['stage', 'is_active', 'tenant']
    search_fields = ['name', 'slug', 'school__name', 'tenant__name']
    autocomplete_fields = ['tenant', 'school']


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ['name', 'school', 'code', 'is_active']
    list_filter = ['is_active', 'tenant']
    search_fields = ['name', 'slug', 'code', 'school__name', 'tenant__name']
    autocomplete_fields = ['tenant', 'school']


@admin.register(ClassGroup)
class ClassGroupAdmin(admin.ModelAdmin):
    list_display = ['name', 'school', 'academic_year', 'grade_level', 'shift', 'max_students', 'is_active']
    list_filter = ['shift', 'is_active', 'tenant', 'academic_year']
    search_fields = ['name', 'slug', 'school__name', 'academic_year__name', 'grade_level__name']
    autocomplete_fields = ['tenant', 'school', 'unit', 'academic_year', 'grade_level']


@admin.register(TeacherProfile)
class TeacherProfileAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'school', 'email', 'registration_number', 'is_active']
    list_filter = ['is_active', 'tenant']
    search_fields = ['full_name', 'email', 'document_number', 'registration_number', 'school__name']
    autocomplete_fields = ['tenant', 'school', 'user']


@admin.register(TeacherAssignment)
class TeacherAssignmentAdmin(admin.ModelAdmin):
    list_display = ['teacher', 'class_group', 'subject', 'academic_year', 'is_active']
    list_filter = ['is_active', 'tenant', 'academic_year', 'subject']
    search_fields = ['teacher__full_name', 'class_group__name', 'subject__name', 'academic_year__name']
    autocomplete_fields = ['tenant', 'teacher', 'class_group', 'subject', 'academic_year']
