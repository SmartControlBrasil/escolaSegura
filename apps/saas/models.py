from django.db import models
from django.utils import timezone


class Tenant(models.Model):
    class Status(models.TextChoices):
        TRIAL = 'TRIAL', 'Trial'
        ACTIVE = 'ACTIVE', 'Ativo'
        PAST_DUE = 'PAST_DUE', 'Pagamento pendente'
        SUSPENDED = 'SUSPENDED', 'Suspenso'
        CANCELED = 'CANCELED', 'Cancelado'

    name = models.CharField(max_length=180)
    slug = models.SlugField(max_length=120, unique=True)
    legal_name = models.CharField(max_length=220, blank=True)
    document_number = models.CharField(max_length=32, blank=True)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=32, blank=True)
    city = models.CharField(max_length=120, blank=True)
    state = models.CharField(max_length=2, blank=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.TRIAL)
    trial_ends_at = models.DateTimeField(null=True, blank=True)
    custom_domain = models.CharField(max_length=180, blank=True)
    subdomain = models.SlugField(max_length=120, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    @property
    def is_blocked(self):
        return not self.is_active or self.status in {
            self.Status.PAST_DUE,
            self.Status.SUSPENDED,
            self.Status.CANCELED,
        }

    @property
    def is_trial_expired(self):
        return bool(self.trial_ends_at and timezone.now() > self.trial_ends_at)


class SubscriptionPlan(models.Model):
    name = models.CharField(max_length=120)
    slug = models.SlugField(max_length=120, unique=True)
    description = models.TextField(blank=True)
    monthly_price = models.DecimalField(max_digits=10, decimal_places=2)
    annual_price = models.DecimalField(max_digits=10, decimal_places=2)
    max_students = models.PositiveIntegerField(default=0)
    max_users = models.PositiveIntegerField(default=0)
    has_academics = models.BooleanField(default=False)
    has_finance = models.BooleanField(default=False)
    has_documents = models.BooleanField(default=False)
    has_ai = models.BooleanField(default=False)
    has_whatsapp = models.BooleanField(default=False)
    has_api = models.BooleanField(default=False)
    display_order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['display_order', 'monthly_price', 'name']

    def __str__(self):
        return self.name

    def includes_feature(self, code):
        return self.features.filter(code=code, is_enabled=True).exists()


class PlanFeature(models.Model):
    plan = models.ForeignKey(SubscriptionPlan, on_delete=models.CASCADE, related_name='features')
    code = models.SlugField(max_length=80)
    name = models.CharField(max_length=120)
    description = models.TextField(blank=True)
    is_enabled = models.BooleanField(default=True)

    class Meta:
        ordering = ['plan__display_order', 'code']
        unique_together = [('plan', 'code')]

    def __str__(self):
        return f'{self.plan} - {self.name}'


class TenantSubscription(models.Model):
    class Status(models.TextChoices):
        TRIAL = 'TRIAL', 'Trial'
        ACTIVE = 'ACTIVE', 'Ativa'
        PAST_DUE = 'PAST_DUE', 'Pagamento pendente'
        SUSPENDED = 'SUSPENDED', 'Suspensa'
        CANCELED = 'CANCELED', 'Cancelada'
        EXPIRED = 'EXPIRED', 'Expirada'

    class BillingCycle(models.TextChoices):
        MONTHLY = 'MONTHLY', 'Mensal'
        YEARLY = 'YEARLY', 'Anual'

    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name='subscriptions')
    plan = models.ForeignKey(SubscriptionPlan, on_delete=models.PROTECT, related_name='subscriptions')
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.TRIAL)
    billing_cycle = models.CharField(max_length=20, choices=BillingCycle.choices, default=BillingCycle.MONTHLY)
    started_at = models.DateTimeField(default=timezone.now)
    trial_ends_at = models.DateTimeField(null=True, blank=True)
    current_period_start = models.DateTimeField(null=True, blank=True)
    current_period_end = models.DateTimeField(null=True, blank=True)
    canceled_at = models.DateTimeField(null=True, blank=True)
    gateway = models.CharField(max_length=60, blank=True)
    gateway_customer_id = models.CharField(max_length=120, blank=True)
    gateway_subscription_id = models.CharField(max_length=120, blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['tenant__name', '-started_at']

    def __str__(self):
        return f'{self.tenant} - {self.plan}'

    @property
    def is_active(self):
        return self.status in {self.Status.TRIAL, self.Status.ACTIVE}

    @property
    def is_past_due(self):
        return self.status == self.Status.PAST_DUE

    @property
    def is_blocked(self):
        return self.status in {
            self.Status.PAST_DUE,
            self.Status.SUSPENDED,
            self.Status.CANCELED,
            self.Status.EXPIRED,
        }

    def can_use_feature(self, code):
        return self.is_active and not self.tenant.is_blocked and self.plan.includes_feature(code)


class TenantUsage(models.Model):
    tenant = models.OneToOneField(Tenant, on_delete=models.CASCADE, related_name='usage')
    students_count = models.PositiveIntegerField(default=0)
    users_count = models.PositiveIntegerField(default=0)
    storage_mb = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['tenant__name']

    def __str__(self):
        return f'Uso de {self.tenant}'

    def is_students_limit_reached(self):
        subscription = self.tenant.subscriptions.filter(
            status__in=[TenantSubscription.Status.TRIAL, TenantSubscription.Status.ACTIVE],
        ).order_by('-started_at').first()
        if not subscription:
            return False
        return self.students_count >= subscription.plan.max_students
