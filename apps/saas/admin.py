from django.contrib import admin

from .models import PlanFeature, SubscriptionPlan, Tenant, TenantSubscription, TenantUsage


class PlanFeatureInline(admin.TabularInline):
    model = PlanFeature
    extra = 0


@admin.register(Tenant)
class TenantAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'status', 'city', 'state', 'is_active']
    list_filter = ['status', 'is_active', 'state']
    search_fields = ['name', 'slug', 'legal_name', 'document_number', 'email']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(SubscriptionPlan)
class SubscriptionPlanAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'monthly_price', 'annual_price', 'max_students', 'is_active']
    list_filter = ['is_active', 'has_academics', 'has_finance', 'has_documents', 'has_ai']
    search_fields = ['name', 'slug', 'description']
    prepopulated_fields = {'slug': ('name',)}
    inlines = [PlanFeatureInline]


@admin.register(PlanFeature)
class PlanFeatureAdmin(admin.ModelAdmin):
    list_display = ['plan', 'code', 'name', 'is_enabled']
    list_filter = ['plan', 'is_enabled']
    search_fields = ['code', 'name', 'description', 'plan__name']


@admin.register(TenantSubscription)
class TenantSubscriptionAdmin(admin.ModelAdmin):
    list_display = ['tenant', 'plan', 'status', 'billing_cycle', 'started_at', 'current_period_end']
    list_filter = ['status', 'billing_cycle', 'plan', 'gateway']
    search_fields = ['tenant__name', 'plan__name', 'gateway_customer_id', 'gateway_subscription_id']


@admin.register(TenantUsage)
class TenantUsageAdmin(admin.ModelAdmin):
    list_display = ['tenant', 'students_count', 'users_count', 'storage_mb']
    search_fields = ['tenant__name', 'tenant__slug']
