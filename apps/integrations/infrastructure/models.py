from django.db import models
from apps.core.infrastructure.models import TimeStampedModel

class IntegrationProvider(TimeStampedModel):
    name = models.CharField(max_length=120)
    slug = models.SlugField(max_length=120, unique=True)
    base_url = models.URLField(blank=True)
    is_active = models.BooleanField(default=True)
    config = models.JSONField(default=dict, blank=True)

    def __str__(self):
        return self.name

class WebhookEvent(TimeStampedModel):
    provider = models.ForeignKey(IntegrationProvider, null=True, blank=True, on_delete=models.SET_NULL)
    event_type = models.CharField(max_length=120)
    payload = models.JSONField(default=dict, blank=True)
    status = models.CharField(max_length=30, default='received')
    processed_at = models.DateTimeField(null=True, blank=True)
    error_message = models.TextField(blank=True)
