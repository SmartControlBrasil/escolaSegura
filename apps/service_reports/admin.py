from django.contrib import admin
from apps.service_reports.infrastructure.models import ServiceReport, ServiceReportItem, ServiceReportPhoto


class ServiceReportItemInline(admin.TabularInline):
    model = ServiceReportItem
    extra = 0
    readonly_fields = ['subtotal']


class ServiceReportPhotoInline(admin.TabularInline):
    model = ServiceReportPhoto
    extra = 0
    fields = ['image','category','caption','technical_notes','taken_at','uploaded_by']


@admin.register(ServiceReport)
class ServiceReportAdmin(admin.ModelAdmin):
    list_display = ['number','title','customer','status','service_date','technician_name','total_amount']
    list_filter = ['status','organization','service_date']
    search_fields = ['number','title','customer__name','technician_name','service_performed']
    readonly_fields = ['total_amount']
    inlines = [ServiceReportItemInline, ServiceReportPhotoInline]


@admin.register(ServiceReportPhoto)
class ServiceReportPhotoAdmin(admin.ModelAdmin):
    list_display = ['report','category','caption','taken_at','uploaded_by']
    list_filter = ['category']
    search_fields = ['report__number','report__title','caption','technical_notes']
