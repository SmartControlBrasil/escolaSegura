from django.contrib import admin
from apps.core.infrastructure.models import ActivityLog, Attachment, Branch, CompanyProfile, Organization, SystemSetting

@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ['name','document','status','created_at']
    search_fields = ['name','document','email']
    list_filter = ['status']

@admin.register(Branch)
class BranchAdmin(admin.ModelAdmin):
    list_display = ['name','organization','city','state','is_headquarters']
    list_filter = ['state','is_headquarters']

@admin.register(SystemSetting)
class SystemSettingAdmin(admin.ModelAdmin):
    list_display = ['key','is_sensitive','updated_at']
    search_fields = ['key','description']

@admin.register(ActivityLog)
class ActivityLogAdmin(admin.ModelAdmin):
    list_display = ['action','actor','organization','object_type','created_at']
    list_filter = ['action','object_type']
    search_fields = ['action','object_id']
    readonly_fields = ['created_at','updated_at']

@admin.register(Attachment)
class AttachmentAdmin(admin.ModelAdmin):
    list_display = ['title','object_type','object_id','uploaded_by','created_at']

@admin.register(CompanyProfile)
class CompanyProfileAdmin(admin.ModelAdmin):
    list_display = ['trade_name', 'organization', 'cnpj', 'is_active']
    search_fields = ['trade_name', 'legal_name', 'cnpj']
