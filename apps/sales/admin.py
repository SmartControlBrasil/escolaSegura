from django.contrib import admin
from apps.sales.infrastructure.models import SalesOrder, SalesOrderItem

class SalesOrderItemInline(admin.TabularInline):
    model = SalesOrderItem
    extra = 0
    readonly_fields = ['subtotal']

@admin.register(SalesOrder)
class SalesOrderAdmin(admin.ModelAdmin):
    list_display = ['number','customer','status','total_amount','created_at']
    list_filter = ['status','created_at']
    search_fields = ['number','customer__name']
    inlines = [SalesOrderItemInline]

@admin.register(SalesOrderItem)
class SalesOrderItemAdmin(admin.ModelAdmin):
    list_display = ['order','product','quantity','unit_price','subtotal']
    search_fields = ['order__number','product__name','product__sku']
