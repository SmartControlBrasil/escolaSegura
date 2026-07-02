from django.contrib import admin

from .models import Assessment, AssessmentGrade, ReportCard, ReportCardEntry, SchoolTerm


@admin.register(SchoolTerm)
class SchoolTermAdmin(admin.ModelAdmin):
    list_display = ['name', 'school', 'academic_year', 'order', 'is_current', 'is_active']
    list_filter = ['is_current', 'is_active', 'academic_year', 'school']
    search_fields = ['name', 'slug']
    autocomplete_fields = ['tenant', 'school', 'academic_year']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Assessment)
class AssessmentAdmin(admin.ModelAdmin):
    list_display = ['title', 'class_group', 'subject', 'assessment_type', 'assessment_date', 'max_score', 'weight', 'is_published']
    list_filter = ['assessment_type', 'is_published', 'academic_year', 'class_group', 'subject']
    search_fields = ['title', 'description', 'class_group__name', 'subject__name']
    autocomplete_fields = ['tenant', 'school', 'academic_year', 'term', 'class_group', 'subject', 'teacher']


@admin.register(AssessmentGrade)
class AssessmentGradeAdmin(admin.ModelAdmin):
    list_display = ['assessment', 'student', 'score', 'is_absent']
    list_filter = ['assessment__subject', 'assessment__class_group', 'is_absent']
    search_fields = ['student__full_name', 'student__student_code', 'assessment__title']
    autocomplete_fields = ['tenant', 'assessment', 'student', 'enrollment']


@admin.register(ReportCard)
class ReportCardAdmin(admin.ModelAdmin):
    list_display = ['student', 'academic_year', 'term', 'status', 'published_at']
    list_filter = ['status', 'academic_year', 'term']
    search_fields = ['student__full_name', 'student__student_code']
    autocomplete_fields = ['tenant', 'school', 'academic_year', 'term', 'student', 'enrollment']


@admin.register(ReportCardEntry)
class ReportCardEntryAdmin(admin.ModelAdmin):
    list_display = ['report_card', 'subject', 'average_score', 'absences_count']
    list_filter = ['subject']
    search_fields = ['report_card__student__full_name', 'subject__name']
    autocomplete_fields = ['tenant', 'report_card', 'subject']
