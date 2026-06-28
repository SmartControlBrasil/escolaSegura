from django.contrib import admin
from apps.inventory.infrastructure.models import StockBalance, StockLocation, StockMovement

@admin.register(StockLocation)
class StockLocationAdmin(admin.ModelAdmin):
    list_display = ['name','code','organization','is_active']
    search_fields = ['name','code']

@admin.register(StockBalance)
class StockBalanceAdmin(admin.ModelAdmin):
    list_display = ['product','location','quantity','minimum_quantity']
    list_filter = ['location']
    search_fields = ['product__name','product__sku']

@admin.register(StockMovement)
class StockMovementAdmin(admin.ModelAdmin):
    list_display = ['product','location','type','quantity','reference','created_at']
    list_filter = ['type','location']
    search_fields = ['product__name','product__sku','reference','reason']
