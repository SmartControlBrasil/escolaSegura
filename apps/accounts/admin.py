from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from apps.accounts.infrastructure.models import User

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (("Smart System", {'fields': ('organization','role','phone','must_change_password')}),)
    list_display = ['username','email','organization','role','is_staff','is_active']
    list_filter = ['role','is_staff','is_active']
