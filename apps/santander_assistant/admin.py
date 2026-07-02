from django.contrib import admin
from apps.santander_assistant.models import (
    SantanderChatMessage,
    SantanderChatSession,
    SantanderKnowledgeItem,
)


class SantanderChatMessageInline(admin.TabularInline):
    model = SantanderChatMessage
    extra = 0
    readonly_fields = ('role', 'content', 'created_at')
    ordering = ('created_at',)


@admin.register(SantanderChatSession)
class SantanderChatSessionAdmin(admin.ModelAdmin):
    list_display = (
        'client_name', 'current_state', 'client_phone',
        'client_email', 'is_active', 'created_at',
    )
    list_filter = ('current_state', 'is_active')
    search_fields = ('client_name', 'client_email', 'client_phone', 'session_key')
    readonly_fields = ('session_key', 'created_at', 'updated_at', 'qualified_at')
    inlines = (SantanderChatMessageInline,)


@admin.register(SantanderKnowledgeItem)
class SantanderKnowledgeItemAdmin(admin.ModelAdmin):
    list_display = ('pergunta', 'categoria', 'is_active')
    list_filter = ('categoria', 'is_active')
    search_fields = ('pergunta', 'resposta', 'tags')
