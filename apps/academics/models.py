from django.conf import settings
from django.db import models
from django.db.models import Q
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


class GradeLevel(TimeStampedModel):
    class Stage(models.TextChoices):
        EARLY_CHILDHOOD = 'EARLY_CHILDHOOD', 'Educação Infantil'
        ELEMENTARY_1 = 'ELEMENTARY_1', 'Fundamental I'
        ELEMENTARY_2 = 'ELEMENTARY_2', 'Fundamental II'
        HIGH_SCHOOL = 'HIGH_SCHOOL', 'Ensino Médio'
        TECHNICAL = 'TECHNICAL', 'Técnico'
        OTHER = 'OTHER', 'Outro'

    tenant = models.ForeignKey('saas.Tenant', on_delete=models.CASCADE, related_name='grade_levels')
    school = models.ForeignKey('schools.School', on_delete=models.CASCADE, related_name='grade_levels')
    name = models.CharField(max_length=120)
    slug = models.SlugField(max_length=120, blank=True)
    order = models.PositiveIntegerField(default=0)
    stage = models.CharField(max_length=30, choices=Stage.choices, default=Stage.OTHER)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order', 'name']
        unique_together = [('school', 'slug')]

    def save(self, *args, **kwargs):
        unique_slug(self, self.name, {'school': self.school})
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Subject(TimeStampedModel):
    tenant = models.ForeignKey('saas.Tenant', on_delete=models.CASCADE, related_name='subjects')
    school = models.ForeignKey('schools.School', on_delete=models.CASCADE, related_name='subjects')
    name = models.CharField(max_length=120)
    slug = models.SlugField(max_length=120, blank=True)
    code = models.CharField(max_length=40, blank=True)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['name']
        unique_together = [('school', 'slug')]

    def save(self, *args, **kwargs):
        unique_slug(self, self.name, {'school': self.school})
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class ClassGroup(TimeStampedModel):
    class Shift(models.TextChoices):
        MORNING = 'MORNING', 'Manhã'
        AFTERNOON = 'AFTERNOON', 'Tarde'
        EVENING = 'EVENING', 'Noite'
        FULL_TIME = 'FULL_TIME', 'Integral'

    tenant = models.ForeignKey('saas.Tenant', on_delete=models.CASCADE, related_name='class_groups')
    school = models.ForeignKey('schools.School', on_delete=models.CASCADE, related_name='class_groups')
    unit = models.ForeignKey('schools.SchoolUnit', null=True, blank=True, on_delete=models.SET_NULL, related_name='class_groups')
    academic_year = models.ForeignKey('schools.AcademicYear', on_delete=models.CASCADE, related_name='class_groups')
    grade_level = models.ForeignKey(GradeLevel, on_delete=models.PROTECT, related_name='class_groups')
    name = models.CharField(max_length=120)
    slug = models.SlugField(max_length=120, blank=True)
    shift = models.CharField(max_length=20, choices=Shift.choices, default=Shift.MORNING)
    max_students = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['academic_year__year', 'name']
        unique_together = [('academic_year', 'slug')]

    def save(self, *args, **kwargs):
        unique_slug(self, self.name, {'academic_year': self.academic_year})
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.academic_year.year} - {self.name}'


class TeacherProfile(TimeStampedModel):
    tenant = models.ForeignKey('saas.Tenant', on_delete=models.CASCADE, related_name='teacher_profiles')
    school = models.ForeignKey('schools.School', on_delete=models.CASCADE, related_name='teacher_profiles')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL, related_name='teacher_profiles')
    full_name = models.CharField(max_length=180)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=32, blank=True)
    document_number = models.CharField(max_length=32, blank=True)
    registration_number = models.CharField(max_length=40, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['full_name']
        constraints = [
            models.UniqueConstraint(
                fields=['school', 'registration_number'],
                condition=~Q(registration_number=''),
                name='uniq_teacher_registration_per_school_when_filled',
            ),
        ]

    def __str__(self):
        return self.full_name


class TeacherAssignment(TimeStampedModel):
    tenant = models.ForeignKey('saas.Tenant', on_delete=models.CASCADE, related_name='teacher_assignments')
    teacher = models.ForeignKey(TeacherProfile, on_delete=models.CASCADE, related_name='assignments')
    class_group = models.ForeignKey(ClassGroup, on_delete=models.CASCADE, related_name='teacher_assignments')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='teacher_assignments')
    academic_year = models.ForeignKey('schools.AcademicYear', on_delete=models.CASCADE, related_name='teacher_assignments')
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['teacher__full_name', 'class_group__name', 'subject__name']
        unique_together = [('teacher', 'class_group', 'subject', 'academic_year')]

    def __str__(self):
        return f'{self.teacher} - {self.class_group} - {self.subject}'
