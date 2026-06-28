from django.contrib import admin
from apps.policy_guard.infrastructure.models import ConsentRecord, DataProcessingRecord, PolicyCheckRun, SecurityIncident

@admin.register(DataProcessingRecord)
class DataProcessingRecordAdmin(admin.ModelAdmin):
    list_display = ['process_name','legal_basis','owner','retention_days','is_active']
    list_filter = ['legal_basis','is_active']
    search_fields = ['process_name','purpose','owner']

@admin.register(ConsentRecord)
class ConsentRecordAdmin(admin.ModelAdmin):
    list_display = ['subject_email','customer','purpose','granted','channel','created_at']
    list_filter = ['granted','channel']

@admin.register(SecurityIncident)
class SecurityIncidentAdmin(admin.ModelAdmin):
    list_display = ['title','severity','status','detected_at','created_at']
    list_filter = ['severity','status']

@admin.register(PolicyCheckRun)
class PolicyCheckRunAdmin(admin.ModelAdmin):
    list_display = ['name','status','score','created_at']
