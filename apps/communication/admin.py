from django.contrib import admin

from .models import (
    Announcement,
    AnnouncementAudience,
    AnnouncementReadReceipt,
    AuthorizationRequest,
    AuthorizationResponse,
    Message,
    MessageThread,
)


@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ['title', 'school', 'priority', 'status', 'published_at', 'expires_at']
    list_filter = ['status', 'priority', 'school', 'published_at']
    search_fields = ['title', 'body']
    autocomplete_fields = ['tenant', 'school', 'unit', 'academic_year', 'created_by']


@admin.register(AnnouncementAudience)
class AnnouncementAudienceAdmin(admin.ModelAdmin):
    list_display = ['announcement', 'audience_type', 'unit', 'class_group', 'student', 'guardian']
    list_filter = ['audience_type']
    autocomplete_fields = ['tenant', 'announcement', 'unit', 'class_group', 'student', 'guardian']


@admin.register(AnnouncementReadReceipt)
class AnnouncementReadReceiptAdmin(admin.ModelAdmin):
    list_display = ['announcement', 'guardian', 'student', 'user', 'channel', 'read_at']
    list_filter = ['channel', 'read_at']
    autocomplete_fields = ['tenant', 'announcement', 'guardian', 'student', 'user']


@admin.register(MessageThread)
class MessageThreadAdmin(admin.ModelAdmin):
    list_display = ['subject', 'school', 'student', 'guardian', 'status', 'priority', 'created_at', 'closed_at']
    list_filter = ['status', 'priority', 'school']
    search_fields = ['subject', 'student__full_name', 'guardian__full_name']
    autocomplete_fields = ['tenant', 'school', 'student', 'guardian', 'created_by']


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['thread', 'sender_user', 'sender_guardian', 'sender_student', 'sent_at', 'read_at']
    list_filter = ['sent_at', 'read_at']
    search_fields = ['body', 'thread__subject']
    autocomplete_fields = ['tenant', 'thread', 'sender_user', 'sender_guardian', 'sender_student']


@admin.register(AuthorizationRequest)
class AuthorizationRequestAdmin(admin.ModelAdmin):
    list_display = ['title', 'student', 'request_type', 'status', 'due_at', 'created_at']
    list_filter = ['request_type', 'status', 'due_at']
    search_fields = ['title', 'description', 'student__full_name']
    autocomplete_fields = ['tenant', 'school', 'student', 'created_by']


@admin.register(AuthorizationResponse)
class AuthorizationResponseAdmin(admin.ModelAdmin):
    list_display = ['request', 'guardian', 'response', 'responded_at']
    list_filter = ['response', 'responded_at']
    search_fields = ['request__title', 'guardian__full_name']
    autocomplete_fields = ['tenant', 'request', 'guardian']
