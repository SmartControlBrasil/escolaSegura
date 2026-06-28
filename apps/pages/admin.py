from django.contrib import admin
from apps.pages.infrastructure.models import HtmlPage

@admin.register(HtmlPage)
class HtmlPageAdmin(admin.ModelAdmin):
    list_display = ['title','slug','organization','status','updated_at']
    list_filter = ['status']
    search_fields = ['title','slug','seo_title']
    prepopulated_fields = {'slug': ('title',)}
