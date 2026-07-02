from django.contrib import admin
from apps.escola_segura_assistant.models import (
    EscolaSeguraChatMessage,
    EscolaSeguraChatSession,
    EscolaSeguraKnowledgeItem,
)


class EscolaSeguraChatMessageInline(admin.TabularInline):
    model = EscolaSeguraChatMessage
    extra = 0
    readonly_fields = ('role', 'content', 'created_at')
    ordering = ('created_at',)


@admin.register(EscolaSeguraChatSession)
class EscolaSeguraChatSessionAdmin(admin.ModelAdmin):
    list_display = (
        'client_name', 'current_state', 'client_phone',
        'client_email', 'is_active', 'created_at',
    )
    list_filter = ('current_state', 'is_active')
    search_fields = ('client_name', 'client_email', 'client_phone', 'session_key')
    readonly_fields = ('session_key', 'created_at', 'updated_at', 'qualified_at')
    inlines = (EscolaSeguraChatMessageInline,)


@admin.register(EscolaSeguraKnowledgeItem)
class EscolaSeguraKnowledgeItemAdmin(admin.ModelAdmin):
    list_display = ('pergunta', 'categoria', 'is_active')
    list_filter = ('categoria', 'is_active')
    search_fields = ('pergunta', 'resposta', 'tags')
