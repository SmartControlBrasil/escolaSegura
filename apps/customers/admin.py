from django.contrib import admin
from apps.customers.infrastructure.models import Customer, CustomerAddress, CustomerContact

class ContactInline(admin.TabularInline):
    model = CustomerContact
    extra = 0

class AddressInline(admin.TabularInline):
    model = CustomerAddress
    extra = 0

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['name','document','email','phone','city','state','status']
    list_filter = ['status','type','state']
    search_fields = ['name','legal_name','document','email','phone']
    inlines = [ContactInline, AddressInline]
