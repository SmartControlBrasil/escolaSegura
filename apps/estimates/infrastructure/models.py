from decimal import Decimal
from django.db import models
from django.utils import timezone
from apps.core.infrastructure.models import TimeStampedModel


class Estimate(TimeStampedModel):
    class Status(models.TextChoices):
        DRAFT = 'draft', 'Rascunho'
        INSPECTION = 'inspection', 'Em vistoria'
        PRICING = 'pricing', 'Em orçamento'
        SENT = 'sent', 'Enviado'
        APPROVED = 'approved', 'Aprovado'
        REJECTED = 'rejected', 'Rejeitado'
        CANCELLED = 'cancelled', 'Cancelado'

    organization = models.ForeignKey('core.Organization', null=True, blank=True, on_delete=models.SET_NULL)
    customer = models.ForeignKey('customers.Customer', null=True, blank=True, on_delete=models.SET_NULL, related_name='estimates')
    sales_order = models.ForeignKey('sales.SalesOrder', null=True, blank=True, on_delete=models.SET_NULL, related_name='estimates')
    number = models.CharField(max_length=40, blank=True, db_index=True)
    title = models.CharField(max_length=180)
    status = models.CharField(max_length=30, choices=Status.choices, default=Status.DRAFT)
    service_location = models.CharField(max_length=240, blank=True)
    visit_scheduled_at = models.DateTimeField(null=True, blank=True)
    scope_summary = models.TextField(blank=True)
    internal_notes = models.TextField(blank=True)
    customer_message = models.TextField(blank=True)
    terms_and_conditions = models.TextField(blank=True)
    validity_days = models.PositiveIntegerField(default=7)
    labor_amount = models.DecimalField(max_digits=14, decimal_places=2, default=Decimal('0.00'))
    discount_amount = models.DecimalField(max_digits=14, decimal_places=2, default=Decimal('0.00'))
    tax_amount = models.DecimalField(max_digits=14, decimal_places=2, default=Decimal('0.00'))
    subtotal_amount = models.DecimalField(max_digits=14, decimal_places=2, default=Decimal('0.00'))
    total_amount = models.DecimalField(max_digits=14, decimal_places=2, default=Decimal('0.00'))
    created_by = models.ForeignKey('accounts.User', null=True, blank=True, on_delete=models.SET_NULL, related_name='created_estimates')
    assigned_to = models.ForeignKey('accounts.User', null=True, blank=True, on_delete=models.SET_NULL, related_name='assigned_estimates')

    class Meta:
        ordering = ['-created_at']

    def recalculate_totals(self):
        items_total = sum((line.subtotal for line in self.lines.all()), Decimal('0.00'))
        self.subtotal_amount = items_total + (self.labor_amount or Decimal('0.00'))
        self.total_amount = self.subtotal_amount + (self.tax_amount or Decimal('0.00')) - (self.discount_amount or Decimal('0.00'))
        if self.total_amount < 0:
            self.total_amount = Decimal('0.00')
        self.save(update_fields=['subtotal_amount', 'total_amount', 'updated_at'])
        return self.total_amount

    def ensure_number(self):
        if not self.number:
            self.number = f'ORC-{str(self.id)[:8].upper()}'
            self.save(update_fields=['number', 'updated_at'])
        return self.number

    def __str__(self):
        return self.number or self.title


class EstimateLine(TimeStampedModel):
    class Kind(models.TextChoices):
        PRODUCT = 'product', 'Produto'
        SERVICE = 'service', 'Serviço'
        MATERIAL = 'material', 'Material'
        LABOR = 'labor', 'Mão de obra'
        OTHER = 'other', 'Outro'

    estimate = models.ForeignKey(Estimate, on_delete=models.CASCADE, related_name='lines')
    product = models.ForeignKey('catalog.Product', null=True, blank=True, on_delete=models.SET_NULL, related_name='estimate_lines')
    kind = models.CharField(max_length=30, choices=Kind.choices, default=Kind.SERVICE)
    description = models.CharField(max_length=240)
    unit = models.CharField(max_length=20, default='un')
    quantity = models.DecimalField(max_digits=12, decimal_places=3, default=Decimal('1.000'))
    unit_price = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'))
    discount_amount = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'))
    subtotal = models.DecimalField(max_digits=14, decimal_places=2, default=Decimal('0.00'))
    sort_order = models.PositiveIntegerField(default=0)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ['sort_order', 'created_at']

    def save(self, *args, **kwargs):
        self.subtotal = ((self.quantity or Decimal('0')) * (self.unit_price or Decimal('0'))) - (self.discount_amount or Decimal('0'))
        if self.subtotal < 0:
            self.subtotal = Decimal('0.00')
        super().save(*args, **kwargs)
        self.estimate.recalculate_totals()

    def __str__(self):
        return self.description


class EstimatePhoto(TimeStampedModel):
    class Category(models.TextChoices):
        BEFORE = 'before', 'Antes do serviço'
        MEASUREMENT = 'measurement', 'Medição'
        ENVIRONMENT = 'environment', 'Ambiente'
        DETAIL = 'detail', 'Detalhe técnico'
        DOCUMENT = 'document', 'Documento'
        OTHER = 'other', 'Outro'

    estimate = models.ForeignKey(Estimate, on_delete=models.CASCADE, related_name='photos')
    image = models.ImageField(upload_to='estimates/photos/%Y/%m/')
    category = models.CharField(max_length=30, choices=Category.choices, default=Category.BEFORE)
    caption = models.CharField(max_length=220, blank=True)
    measurement_notes = models.TextField(blank=True)
    taken_at = models.DateTimeField(default=timezone.now)
    uploaded_by = models.ForeignKey('accounts.User', null=True, blank=True, on_delete=models.SET_NULL)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)

    class Meta:
        ordering = ['-taken_at']

    def __str__(self):
        return self.caption or f'Foto {self.estimate}'


class EstimateMeasurement(TimeStampedModel):
    estimate = models.ForeignKey(Estimate, on_delete=models.CASCADE, related_name='measurements')
    label = models.CharField(max_length=160)
    value = models.DecimalField(max_digits=12, decimal_places=3)
    unit = models.CharField(max_length=20, default='m')
    notes = models.TextField(blank=True)
    sort_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['sort_order', 'created_at']

    def __str__(self):
        return f'{self.label}: {self.value} {self.unit}'


class EstimateContactMessage(TimeStampedModel):
    class Channel(models.TextChoices):
        WHATSAPP = 'whatsapp', 'WhatsApp'
        EMAIL = 'email', 'E-mail'
        PHONE = 'phone', 'Telefone'
        INTERNAL = 'internal', 'Interno'

    class Status(models.TextChoices):
        DRAFT = 'draft', 'Rascunho'
        APPROVED = 'approved', 'Aprovado'
        SENT = 'sent', 'Enviado'
        CANCELLED = 'cancelled', 'Cancelado'

    estimate = models.ForeignKey(Estimate, on_delete=models.CASCADE, related_name='contact_messages')
    channel = models.CharField(max_length=30, choices=Channel.choices, default=Channel.WHATSAPP)
    subject = models.CharField(max_length=180, blank=True)
    body = models.TextField()
    status = models.CharField(max_length=30, choices=Status.choices, default=Status.DRAFT)
    approved_by_human = models.BooleanField(default=False)
    sent_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.get_channel_display()} - {self.estimate}'
