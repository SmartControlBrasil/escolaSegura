from decimal import Decimal
from django.db import models
from django.utils import timezone
from apps.core.infrastructure.models import TimeStampedModel


class ServiceReport(TimeStampedModel):
    class Status(models.TextChoices):
        DRAFT = 'draft', 'Rascunho'
        IN_PROGRESS = 'in_progress', 'Em execução'
        COMPLETED = 'completed', 'Concluído'
        DELIVERED = 'delivered', 'Entregue'
        APPROVED = 'approved', 'Aprovado pelo cliente'
        CANCELLED = 'cancelled', 'Cancelado'

    organization = models.ForeignKey('core.Organization', null=True, blank=True, on_delete=models.SET_NULL)
    customer = models.ForeignKey('customers.Customer', on_delete=models.PROTECT, related_name='service_reports')
    estimate = models.ForeignKey('estimates.Estimate', null=True, blank=True, on_delete=models.SET_NULL, related_name='service_reports')
    sales_order = models.ForeignKey('sales.SalesOrder', null=True, blank=True, on_delete=models.SET_NULL, related_name='service_reports')
    number = models.CharField(max_length=40, blank=True, db_index=True)
    title = models.CharField(max_length=180)
    status = models.CharField(max_length=30, choices=Status.choices, default=Status.DRAFT)
    service_date = models.DateField(default=timezone.localdate)
    service_location = models.CharField(max_length=240, blank=True)
    technician_name = models.CharField(max_length=160, blank=True)
    problem_reported = models.TextField(blank=True)
    service_performed = models.TextField(blank=True)
    recommendations = models.TextField(blank=True)
    customer_signature_name = models.CharField(max_length=160, blank=True)
    started_at = models.DateTimeField(null=True, blank=True)
    finished_at = models.DateTimeField(null=True, blank=True)
    total_amount = models.DecimalField(max_digits=14, decimal_places=2, default=Decimal('0.00'))
    created_by = models.ForeignKey('accounts.User', null=True, blank=True, on_delete=models.SET_NULL)

    class Meta:
        ordering = ['-service_date', '-created_at']

    def ensure_number(self):
        if not self.number:
            self.number = f'RDS-{str(self.id)[:8].upper()}'
            self.save(update_fields=['number', 'updated_at'])
        return self.number

    def recalculate_total(self):
        self.total_amount = sum((item.subtotal for item in self.items.filter(is_billable=True)), Decimal('0.00'))
        self.save(update_fields=['total_amount','updated_at'])
        return self.total_amount

    def __str__(self):
        return self.number or self.title


class ServiceReportItem(TimeStampedModel):
    report = models.ForeignKey(ServiceReport, on_delete=models.CASCADE, related_name='items')
    description = models.CharField(max_length=240)
    quantity = models.DecimalField(max_digits=12, decimal_places=3, default=Decimal('1.000'))
    unit = models.CharField(max_length=20, default='h')
    unit_price = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'))
    subtotal = models.DecimalField(max_digits=14, decimal_places=2, default=Decimal('0.00'))
    is_billable = models.BooleanField(default=True)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ['created_at']

    def save(self, *args, **kwargs):
        self.subtotal = (self.quantity or Decimal('0')) * (self.unit_price or Decimal('0'))
        super().save(*args, **kwargs)
        self.report.recalculate_total()

    def __str__(self):
        return self.description


class ServiceReportPhoto(TimeStampedModel):
    class Category(models.TextChoices):
        BEFORE = 'before', 'Antes'
        DURING = 'during', 'Durante'
        AFTER = 'after', 'Depois'
        EVIDENCE = 'evidence', 'Evidência técnica'
        DOCUMENT = 'document', 'Documento'
        OTHER = 'other', 'Outro'

    report = models.ForeignKey(ServiceReport, on_delete=models.CASCADE, related_name='photos')
    image = models.ImageField(upload_to='service-reports/photos/%Y/%m/')
    category = models.CharField(max_length=30, choices=Category.choices, default=Category.EVIDENCE)
    caption = models.CharField(max_length=220, blank=True)
    technical_notes = models.TextField(blank=True)
    taken_at = models.DateTimeField(default=timezone.now)
    uploaded_by = models.ForeignKey('accounts.User', null=True, blank=True, on_delete=models.SET_NULL)

    class Meta:
        ordering = ['-taken_at']

    def __str__(self):
        return self.caption or f'Foto {self.report}'
