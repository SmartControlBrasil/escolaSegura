from decimal import Decimal
from django.db import models
from apps.core.infrastructure.models import TimeStampedModel

class SalesOrder(TimeStampedModel):
    class Status(models.TextChoices):
        DRAFT = 'draft', 'Rascunho'
        CONFIRMED = 'confirmed', 'Confirmado'
        CANCELLED = 'cancelled', 'Cancelado'
        COMPLETED = 'completed', 'Concluído'

    organization = models.ForeignKey('core.Organization', null=True, blank=True, on_delete=models.SET_NULL)
    customer = models.ForeignKey('customers.Customer', on_delete=models.PROTECT, related_name='sales_orders')
    number = models.CharField(max_length=40, blank=True, db_index=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.DRAFT)
    total_amount = models.DecimalField(max_digits=14, decimal_places=2, default=Decimal('0.00'))
    notes = models.TextField(blank=True)
    created_by = models.ForeignKey('accounts.User', null=True, blank=True, on_delete=models.SET_NULL)

    class Meta:
        ordering = ['-created_at']

    def recalculate_total(self):
        total = sum((item.subtotal for item in self.items.all()), Decimal('0.00'))
        self.total_amount = total
        self.save(update_fields=['total_amount', 'updated_at'])
        return total

    def __str__(self):
        return self.number or str(self.id)

class SalesOrderItem(TimeStampedModel):
    order = models.ForeignKey(SalesOrder, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey('catalog.Product', on_delete=models.PROTECT, related_name='sales_order_items')
    description = models.CharField(max_length=220, blank=True)
    quantity = models.DecimalField(max_digits=12, decimal_places=3)
    unit_price = models.DecimalField(max_digits=12, decimal_places=2)
    subtotal = models.DecimalField(max_digits=14, decimal_places=2, default=Decimal('0.00'))

    class Meta:
        ordering = ['created_at']

    def save(self, *args, **kwargs):
        self.subtotal = (self.quantity or Decimal('0')) * (self.unit_price or Decimal('0'))
        super().save(*args, **kwargs)


class Project(TimeStampedModel):
    class Status(models.TextChoices):
        PLANNED = 'planned', 'Planejada'
        PRODUCTION = 'production', 'Em produção'
        INSTALLATION = 'installation', 'Em instalação'
        DELIVERED = 'delivered', 'Entregue'
        PAUSED = 'paused', 'Pausada'
        CANCELLED = 'cancelled', 'Cancelada'

    organization = models.ForeignKey('core.Organization', null=True, blank=True, on_delete=models.SET_NULL)
    customer = models.ForeignKey('customers.Customer', on_delete=models.PROTECT, related_name='projects')
    estimate = models.ForeignKey('estimates.Estimate', null=True, blank=True, on_delete=models.SET_NULL, related_name='projects')
    title = models.CharField(max_length=180)
    address = models.CharField(max_length=240, blank=True)
    responsible = models.ForeignKey('accounts.User', null=True, blank=True, on_delete=models.SET_NULL, related_name='managed_projects')
    scheduled_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=30, choices=Status.choices, default=Status.PLANNED)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ['-scheduled_date', '-created_at']

    def __str__(self):
        return self.title
