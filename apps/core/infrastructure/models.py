import uuid
from django.conf import settings
from django.db import models
from django.utils import timezone

class TimeStampedModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Organization(TimeStampedModel):
    class Status(models.TextChoices):
        ACTIVE = 'active', 'Ativa'
        INACTIVE = 'inactive', 'Inativa'

    name = models.CharField(max_length=180)
    legal_name = models.CharField(max_length=220, blank=True)
    document = models.CharField(max_length=32, blank=True, db_index=True)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=32, blank=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.ACTIVE)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

class Branch(TimeStampedModel):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='branches')
    name = models.CharField(max_length=160)
    city = models.CharField(max_length=120, blank=True)
    state = models.CharField(max_length=2, blank=True)
    is_headquarters = models.BooleanField(default=False)

    class Meta:
        ordering = ['organization__name', 'name']
        unique_together = [('organization', 'name')]

    def __str__(self):
        return f'{self.organization} / {self.name}'

class SystemSetting(TimeStampedModel):
    key = models.SlugField(max_length=120, unique=True)
    value = models.JSONField(default=dict, blank=True)
    description = models.TextField(blank=True)
    is_sensitive = models.BooleanField(default=False)

    class Meta:
        ordering = ['key']

    def __str__(self):
        return self.key

class ActivityLog(TimeStampedModel):
    actor = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL)
    organization = models.ForeignKey(Organization, null=True, blank=True, on_delete=models.SET_NULL)
    action = models.CharField(max_length=120, db_index=True)
    object_type = models.CharField(max_length=120, blank=True)
    object_id = models.CharField(max_length=80, blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)
    metadata = models.JSONField(default=dict, blank=True)

    class Meta:
        ordering = ['-created_at']

class Attachment(TimeStampedModel):
    organization = models.ForeignKey(Organization, null=True, blank=True, on_delete=models.SET_NULL)
    uploaded_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL)
    file = models.FileField(upload_to='attachments/%Y/%m/')
    title = models.CharField(max_length=180, blank=True)
    content_type = models.CharField(max_length=120, blank=True)
    object_type = models.CharField(max_length=120, blank=True)
    object_id = models.CharField(max_length=80, blank=True)

    class Meta:
        ordering = ['-created_at']
