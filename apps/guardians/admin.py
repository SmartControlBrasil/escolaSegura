from django.contrib import admin

from .models import Guardian, GuardianStudentLink


@admin.register(Guardian)
class GuardianAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'school', 'email', 'phone', 'is_active']
    list_filter = ['is_active', 'tenant']
    search_fields = ['full_name', 'email', 'phone', 'document_number', 'school__name']
    autocomplete_fields = ['tenant', 'school']


@admin.register(GuardianStudentLink)
class GuardianStudentLinkAdmin(admin.ModelAdmin):
    list_display = ['guardian', 'student', 'relationship', 'is_primary', 'can_pickup', 'can_receive_messages', 'is_active']
    list_filter = ['relationship', 'is_primary', 'is_active', 'tenant']
    search_fields = ['guardian__full_name', 'student__full_name']
    autocomplete_fields = ['tenant', 'guardian', 'student']
