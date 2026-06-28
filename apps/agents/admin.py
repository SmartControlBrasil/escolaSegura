from django.contrib import admin
from apps.agents.infrastructure.models import AgentProfile, AtlasEmailDraft, AtlasProspect, VirtualAssistantMessage, VirtualAssistantSession

@admin.register(AgentProfile)
class AgentProfileAdmin(admin.ModelAdmin):
    list_display = ['name','kind','is_active']
    list_filter = ['kind','is_active']

@admin.register(VirtualAssistantSession)
class VirtualAssistantSessionAdmin(admin.ModelAdmin):
    list_display = ['visitor_name','visitor_email','visitor_phone','channel','status','created_at']
    search_fields = ['visitor_name','visitor_email','visitor_phone','summary']

@admin.register(VirtualAssistantMessage)
class VirtualAssistantMessageAdmin(admin.ModelAdmin):
    list_display = ['session','role','created_at']
    search_fields = ['content']

@admin.register(AtlasProspect)
class AtlasProspectAdmin(admin.ModelAdmin):
    list_display = ['company_name','contact_email','city','state','score','status']
    list_filter = ['status','state']
    search_fields = ['company_name','website','contact_email']

@admin.register(AtlasEmailDraft)
class AtlasEmailDraftAdmin(admin.ModelAdmin):
    list_display = ['prospect','to_email','subject','approved_by_human','status','sent_at']
    list_filter = ['approved_by_human','status']
