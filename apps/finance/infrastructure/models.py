from decimal import Decimal
from django.db import models
from apps.core.infrastructure.models import TimeStampedModel

class FinancialStatus(models.TextChoices):
    PENDING = 'pending', 'Pendente'
    PAID = 'paid', 'Pago'
    OVERDUE = 'overdue', 'Vencido'
    CANCELLED = 'cancelled', 'Cancelado'

class AccountReceivable(TimeStampedModel):
    organization = models.ForeignKey('core.Organization', null=True, blank=True, on_delete=models.SET_NULL)
    customer = models.ForeignKey('customers.Customer', null=True, blank=True, on_delete=models.SET_NULL, related_name='receivables')
    description = models.CharField(max_length=220)
    amount = models.DecimalField(max_digits=14, decimal_places=2, default=Decimal('0.00'))
    issue_date = models.DateField(null=True, blank=True)
    due_date = models.DateField()
    paid_at = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=FinancialStatus.choices, default=FinancialStatus.PENDING)
    reference = models.CharField(max_length=120, blank=True)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ['due_date']

    def __str__(self):
        return f'{self.description} - {self.amount}'

class AccountPayable(TimeStampedModel):
    organization = models.ForeignKey('core.Organization', null=True, blank=True, on_delete=models.SET_NULL)
    supplier_name = models.CharField(max_length=180, blank=True)
    description = models.CharField(max_length=220)
    amount = models.DecimalField(max_digits=14, decimal_places=2, default=Decimal('0.00'))
    issue_date = models.DateField(null=True, blank=True)
    due_date = models.DateField()
    paid_at = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=FinancialStatus.choices, default=FinancialStatus.PENDING)
    reference = models.CharField(max_length=120, blank=True)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ['due_date']

    def __str__(self):
        return f'{self.description} - {self.amount}'
