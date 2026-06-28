from django.contrib import admin
from apps.finance.infrastructure.models import AccountPayable, AccountReceivable

@admin.register(AccountReceivable)
class AccountReceivableAdmin(admin.ModelAdmin):
    list_display = ['description','customer','amount','due_date','status']
    list_filter = ['status','due_date']
    search_fields = ['description','reference','customer__name']

@admin.register(AccountPayable)
class AccountPayableAdmin(admin.ModelAdmin):
    list_display = ['description','supplier_name','amount','due_date','status']
    list_filter = ['status','due_date']
    search_fields = ['description','reference','supplier_name']
