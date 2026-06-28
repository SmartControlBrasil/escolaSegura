from django.db import models
from apps.core.infrastructure.models import TimeStampedModel

class Customer(TimeStampedModel):
    class Type(models.TextChoices):
        PERSON = 'person', 'Pessoa Física'
        COMPANY = 'company', 'Pessoa Jurídica'

    class Status(models.TextChoices):
        ACTIVE = 'active', 'Ativo'
        INACTIVE = 'inactive', 'Inativo'
        PROSPECT = 'prospect', 'Prospect'

    organization = models.ForeignKey('core.Organization', null=True, blank=True, on_delete=models.SET_NULL)
    type = models.CharField(max_length=20, choices=Type.choices, default=Type.COMPANY)
    name = models.CharField(max_length=180)
    legal_name = models.CharField(max_length=220, blank=True)
    document = models.CharField(max_length=32, blank=True, db_index=True)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=32, blank=True)
    city = models.CharField(max_length=120, blank=True)
    state = models.CharField(max_length=2, blank=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.ACTIVE)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ['name']
        indexes = [models.Index(fields=['organization','document'])]

    def __str__(self):
        return self.name

class CustomerContact(TimeStampedModel):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='contacts')
    name = models.CharField(max_length=160)
    role = models.CharField(max_length=120, blank=True)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=32, blank=True)
    is_primary = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.name} - {self.customer}'

class CustomerAddress(TimeStampedModel):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='addresses')
    label = models.CharField(max_length=80, default='Principal')
    street = models.CharField(max_length=180, blank=True)
    number = models.CharField(max_length=30, blank=True)
    complement = models.CharField(max_length=120, blank=True)
    district = models.CharField(max_length=120, blank=True)
    city = models.CharField(max_length=120, blank=True)
    state = models.CharField(max_length=2, blank=True)
    zipcode = models.CharField(max_length=20, blank=True)
