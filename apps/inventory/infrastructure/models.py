from decimal import Decimal
from django.core.exceptions import ValidationError
from django.db import models, transaction
from apps.core.infrastructure.models import TimeStampedModel

class StockLocation(TimeStampedModel):
    organization = models.ForeignKey('core.Organization', null=True, blank=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=160)
    code = models.CharField(max_length=40, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['name']
        unique_together = [('organization','code')]

    def __str__(self):
        return self.name

class StockBalance(TimeStampedModel):
    product = models.ForeignKey('catalog.Product', on_delete=models.CASCADE, related_name='stock_balances')
    location = models.ForeignKey(StockLocation, on_delete=models.CASCADE, related_name='balances')
    quantity = models.DecimalField(max_digits=14, decimal_places=3, default=Decimal('0.000'))
    minimum_quantity = models.DecimalField(max_digits=14, decimal_places=3, default=Decimal('0.000'))

    class Meta:
        unique_together = [('product','location')]

    def __str__(self):
        return f'{self.product} @ {self.location}: {self.quantity}'

class StockMovement(TimeStampedModel):
    class Type(models.TextChoices):
        IN = 'in', 'Entrada'
        OUT = 'out', 'Saída'
        ADJUST = 'adjust', 'Ajuste'

    product = models.ForeignKey('catalog.Product', on_delete=models.PROTECT, related_name='stock_movements')
    location = models.ForeignKey(StockLocation, on_delete=models.PROTECT, related_name='movements')
    type = models.CharField(max_length=20, choices=Type.choices)
    quantity = models.DecimalField(max_digits=14, decimal_places=3)
    reason = models.CharField(max_length=160, blank=True)
    reference = models.CharField(max_length=120, blank=True)
    created_by = models.ForeignKey('accounts.User', null=True, blank=True, on_delete=models.SET_NULL)

    class Meta:
        ordering = ['-created_at']

    def clean(self):
        if self.quantity <= 0:
            raise ValidationError('Quantidade deve ser maior que zero.')

    def apply(self):
        self.clean()
        with transaction.atomic():
            balance, _ = StockBalance.objects.select_for_update().get_or_create(
                product=self.product,
                location=self.location,
                defaults={'quantity': Decimal('0.000')},
            )
            if self.type == self.Type.IN:
                balance.quantity += self.quantity
            elif self.type == self.Type.OUT:
                if balance.quantity < self.quantity:
                    raise ValidationError('Estoque insuficiente para saída.')
                balance.quantity -= self.quantity
            elif self.type == self.Type.ADJUST:
                balance.quantity = self.quantity
            balance.save()
            self.save()
            return self
