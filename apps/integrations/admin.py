from django.contrib import admin
from apps.integrations.infrastructure.models import IntegrationProvider, WebhookEvent

@admin.register(IntegrationProvider)
class IntegrationProviderAdmin(admin.ModelAdmin):
    list_display = ['name','slug','base_url','is_active']
    prepopulated_fields = {'slug': ('name',)}

@admin.register(WebhookEvent)
class WebhookEventAdmin(admin.ModelAdmin):
    list_display = ['event_type','provider','status','processed_at','created_at']
    list_filter = ['status','event_type']
