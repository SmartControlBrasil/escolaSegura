from django.core.exceptions import ValidationError
from django.db import models
from django.utils.text import slugify


def unique_slug(instance, source, scope_filter):
    if instance.slug:
        return
    base_slug = slugify(source) or 'registro'
    slug = base_slug
    counter = 2
    model = instance.__class__
    while model.objects.filter(slug=slug, **scope_filter).exclude(pk=instance.pk).exists():
        slug = f'{base_slug}-{counter}'
        counter += 1
    instance.slug = slug


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class School(TimeStampedModel):
    tenant = models.ForeignKey('saas.Tenant', on_delete=models.CASCADE, related_name='schools')
    name = models.CharField(max_length=180)
    slug = models.SlugField(max_length=120, blank=True)
    legal_name = models.CharField(max_length=220, blank=True)
    document_number = models.CharField(max_length=32, blank=True)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=32, blank=True)
    website = models.URLField(blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['name']
        unique_together = [('tenant', 'slug')]

    def save(self, *args, **kwargs):
        unique_slug(self, self.name, {'tenant': self.tenant})
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class SchoolUnit(TimeStampedModel):
    tenant = models.ForeignKey('saas.Tenant', on_delete=models.CASCADE, related_name='school_units')
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name='units')
    name = models.CharField(max_length=180)
    slug = models.SlugField(max_length=120, blank=True)
    code = models.CharField(max_length=40, blank=True)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=32, blank=True)
    address_line = models.CharField(max_length=220, blank=True)
    city = models.CharField(max_length=120, blank=True)
    state = models.CharField(max_length=2, blank=True)
    postal_code = models.CharField(max_length=20, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['school__name', 'name']
        unique_together = [('school', 'slug')]

    def save(self, *args, **kwargs):
        unique_slug(self, self.name, {'school': self.school})
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.school} - {self.name}'


class AcademicYear(TimeStampedModel):
    tenant = models.ForeignKey('saas.Tenant', on_delete=models.CASCADE, related_name='academic_years')
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name='academic_years')
    name = models.CharField(max_length=120)
    year = models.PositiveIntegerField()
    starts_at = models.DateField()
    ends_at = models.DateField()
    is_current = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['-year', 'school__name']
        unique_together = [('school', 'year')]

    def clean(self):
        super().clean()
        if self.starts_at and self.ends_at and self.ends_at < self.starts_at:
            raise ValidationError({'ends_at': 'A data de fim deve ser igual ou posterior ao início.'})

    def __str__(self):
        return f'{self.school} - {self.year}'
