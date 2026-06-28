from django.contrib import admin
from apps.estimates.infrastructure.models import Estimate, EstimateContactMessage, EstimateLine, EstimateMeasurement, EstimatePhoto


class EstimateLineInline(admin.TabularInline):
    model = EstimateLine
    extra = 0
    fields = ['kind','product','description','unit','quantity','unit_price','discount_amount','subtotal','sort_order']
    readonly_fields = ['subtotal']


class EstimatePhotoInline(admin.TabularInline):
    model = EstimatePhoto
    extra = 0
    fields = ['image','category','caption','measurement_notes','taken_at','uploaded_by']


class EstimateMeasurementInline(admin.TabularInline):
    model = EstimateMeasurement
    extra = 0
    fields = ['label','value','unit','notes','sort_order']


@admin.register(Estimate)
class EstimateAdmin(admin.ModelAdmin):
    list_display = ['number','title','customer','status','total_amount','visit_scheduled_at','created_at']
    list_filter = ['status','organization','assigned_to']
    search_fields = ['number','title','customer__name','scope_summary','service_location']
    readonly_fields = ['subtotal_amount','total_amount']
    inlines = [EstimateLineInline, EstimateMeasurementInline, EstimatePhotoInline]


@admin.register(EstimateContactMessage)
class EstimateContactMessageAdmin(admin.ModelAdmin):
    list_display = ['estimate','channel','status','approved_by_human','sent_at','created_at']
    list_filter = ['channel','status','approved_by_human']
    search_fields = ['subject','body','estimate__number']
