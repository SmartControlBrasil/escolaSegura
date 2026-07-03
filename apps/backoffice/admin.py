from django.contrib import admin

from .models import Guardian, SchoolUnit, Student, StudentGuardianLink


@admin.register(SchoolUnit)
class SchoolUnitAdmin(admin.ModelAdmin):
    list_display = ('name', 'city', 'state', 'is_active', 'updated_at')
    list_filter = ('is_active', 'state')
    search_fields = ('name', 'legal_name', 'document', 'city')
    prepopulated_fields = {'slug': ('name',)}


class StudentGuardianLinkInline(admin.TabularInline):
    model = StudentGuardianLink
    extra = 0
    autocomplete_fields = ('guardian',)


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'registration_code', 'school_unit', 'grade_name', 'classroom', 'status')
    list_filter = ('status', 'school_unit')
    search_fields = ('full_name', 'registration_code', 'school_unit__name')
    autocomplete_fields = ('school_unit',)
    inlines = (StudentGuardianLinkInline,)


@admin.register(Guardian)
class GuardianAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'phone', 'email', 'document', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('full_name', 'email', 'phone', 'document')


@admin.register(StudentGuardianLink)
class StudentGuardianLinkAdmin(admin.ModelAdmin):
    list_display = (
        'student',
        'guardian',
        'relationship',
        'is_primary',
        'can_authorize_exit',
        'can_receive_notifications',
        'can_approve_canteen_orders',
    )
    list_filter = ('relationship', 'is_primary', 'can_authorize_exit', 'can_receive_notifications')
    search_fields = ('student__full_name', 'guardian__full_name')
    autocomplete_fields = ('student', 'guardian')
