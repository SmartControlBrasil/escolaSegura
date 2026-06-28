from django.db import models
from apps.core.infrastructure.models import TimeStampedModel

class HtmlPage(TimeStampedModel):
    class Status(models.TextChoices):
        DRAFT = 'draft', 'Rascunho'
        PUBLISHED = 'published', 'Publicada'
        ARCHIVED = 'archived', 'Arquivada'

    organization = models.ForeignKey('core.Organization', null=True, blank=True, on_delete=models.SET_NULL)
    title = models.CharField(max_length=180)
    slug = models.SlugField(max_length=180)
    template_name = models.CharField(max_length=180, default='pages/generic.html')
    html = models.TextField(blank=True)
    content = models.JSONField(default=dict, blank=True)
    seo_title = models.CharField(max_length=180, blank=True)
    seo_description = models.CharField(max_length=260, blank=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.DRAFT)

    class Meta:
        ordering = ['title']
        unique_together = [('organization','slug')]

    def __str__(self):
        return self.title
