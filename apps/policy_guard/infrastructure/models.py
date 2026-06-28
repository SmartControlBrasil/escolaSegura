from django.db import models
from apps.core.infrastructure.models import TimeStampedModel

class DataProcessingRecord(TimeStampedModel):
    process_name = models.CharField(max_length=180)
    legal_basis = models.CharField(max_length=120)
    data_categories = models.JSONField(default=list, blank=True)
    purpose = models.TextField()
    retention_days = models.PositiveIntegerField(default=365)
    owner = models.CharField(max_length=160, blank=True)
    is_active = models.BooleanField(default=True)

class ConsentRecord(TimeStampedModel):
    customer = models.ForeignKey('customers.Customer', null=True, blank=True, on_delete=models.SET_NULL)
    subject_email = models.EmailField(blank=True)
    channel = models.CharField(max_length=60, default='web')
    purpose = models.CharField(max_length=180)
    granted = models.BooleanField(default=False)
    evidence = models.JSONField(default=dict, blank=True)

class SecurityIncident(TimeStampedModel):
    class Severity(models.TextChoices):
        LOW = 'low', 'Baixa'
        MEDIUM = 'medium', 'Média'
        HIGH = 'high', 'Alta'
        CRITICAL = 'critical', 'Crítica'

    title = models.CharField(max_length=180)
    severity = models.CharField(max_length=20, choices=Severity.choices, default=Severity.LOW)
    description = models.TextField()
    status = models.CharField(max_length=30, default='open')
    detected_at = models.DateTimeField(null=True, blank=True)
    closed_at = models.DateTimeField(null=True, blank=True)
    mitigation = models.TextField(blank=True)

class PolicyCheckRun(TimeStampedModel):
    name = models.CharField(max_length=180)
    status = models.CharField(max_length=30, default='pending')
    findings = models.JSONField(default=list, blank=True)
    score = models.PositiveSmallIntegerField(default=0)
