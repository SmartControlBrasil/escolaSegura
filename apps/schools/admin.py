from django.contrib import admin

from .models import AcademicYear, School, SchoolUnit


@admin.register(School)
class SchoolAdmin(admin.ModelAdmin):
    list_display = ['name', 'tenant', 'slug', 'email', 'is_active']
    list_filter = ['is_active', 'tenant']
    search_fields = ['name', 'slug', 'legal_name', 'document_number', 'email']
    autocomplete_fields = ['tenant']


@admin.register(SchoolUnit)
class SchoolUnitAdmin(admin.ModelAdmin):
    list_display = ['name', 'school', 'tenant', 'code', 'city', 'state', 'is_active']
    list_filter = ['is_active', 'state', 'tenant']
    search_fields = ['name', 'slug', 'code', 'school__name', 'tenant__name']
    autocomplete_fields = ['tenant', 'school']


@admin.register(AcademicYear)
class AcademicYearAdmin(admin.ModelAdmin):
    list_display = ['name', 'school', 'year', 'starts_at', 'ends_at', 'is_current', 'is_active']
    list_filter = ['year', 'is_current', 'is_active', 'tenant']
    search_fields = ['name', 'school__name', 'tenant__name']
    autocomplete_fields = ['tenant', 'school']
