from decimal import Decimal

from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from django.utils.text import slugify


def unique_slug(instance, source, scope_filter):
    if instance.slug:
        return
    base_slug = slugify(source) or 'etapa'
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


class SchoolTerm(TimeStampedModel):
    tenant = models.ForeignKey('saas.Tenant', on_delete=models.CASCADE, related_name='school_terms')
    school = models.ForeignKey('schools.School', on_delete=models.CASCADE, related_name='school_terms')
    academic_year = models.ForeignKey('schools.AcademicYear', on_delete=models.CASCADE, related_name='school_terms')
    name = models.CharField(max_length=120)
    slug = models.SlugField(max_length=120, blank=True)
    order = models.PositiveIntegerField(default=1)
    starts_at = models.DateField(null=True, blank=True)
    ends_at = models.DateField(null=True, blank=True)
    is_current = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['academic_year', 'order']
        unique_together = [('academic_year', 'slug')]

    def clean(self):
        super().clean()
        if self.starts_at and self.ends_at and self.ends_at < self.starts_at:
            raise ValidationError({'ends_at': 'A data de fim deve ser igual ou posterior ao início.'})

    def save(self, *args, **kwargs):
        unique_slug(self, self.name, {'academic_year': self.academic_year})
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.academic_year} - {self.name}'


class Assessment(TimeStampedModel):
    class AssessmentType(models.TextChoices):
        TEST = 'TEST', 'Prova'
        ASSIGNMENT = 'ASSIGNMENT', 'Trabalho'
        PARTICIPATION = 'PARTICIPATION', 'Participação'
        PROJECT = 'PROJECT', 'Projeto'
        SIMULATION = 'SIMULATION', 'Simulado'
        RECOVERY = 'RECOVERY', 'Recuperação'
        OTHER = 'OTHER', 'Outro'

    tenant = models.ForeignKey('saas.Tenant', on_delete=models.CASCADE, related_name='assessments')
    school = models.ForeignKey('schools.School', on_delete=models.CASCADE, related_name='assessments')
    academic_year = models.ForeignKey('schools.AcademicYear', on_delete=models.CASCADE, related_name='assessments')
    term = models.ForeignKey(SchoolTerm, null=True, blank=True, on_delete=models.SET_NULL, related_name='assessments')
    class_group = models.ForeignKey('academics.ClassGroup', on_delete=models.CASCADE, related_name='assessments')
    subject = models.ForeignKey('academics.Subject', on_delete=models.CASCADE, related_name='assessments')
    teacher = models.ForeignKey('academics.TeacherProfile', null=True, blank=True, on_delete=models.SET_NULL, related_name='assessments')
    title = models.CharField(max_length=180)
    description = models.TextField(blank=True)
    assessment_type = models.CharField(max_length=20, choices=AssessmentType.choices, default=AssessmentType.TEST)
    assessment_date = models.DateField(null=True, blank=True)
    max_score = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal('10.00'))
    weight = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal('1.00'))
    is_published = models.BooleanField(default=False)
    published_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-assessment_date', 'title']

    def clean(self):
        super().clean()
        if self.max_score is not None and self.max_score <= 0:
            raise ValidationError({'max_score': 'A pontuação máxima deve ser maior que zero.'})
        if self.weight is not None and self.weight <= 0:
            raise ValidationError({'weight': 'O peso deve ser maior que zero.'})

    def __str__(self):
        return f'{self.title} - {self.class_group} - {self.subject}'

    def publish(self):
        self.is_published = True
        if self.published_at is None:
            self.published_at = timezone.now()
        self.save(update_fields=['is_published', 'published_at', 'updated_at'])


class AssessmentGrade(TimeStampedModel):
    tenant = models.ForeignKey('saas.Tenant', on_delete=models.CASCADE, related_name='assessment_grades')
    assessment = models.ForeignKey(Assessment, on_delete=models.CASCADE, related_name='grades')
    student = models.ForeignKey('students.Student', on_delete=models.CASCADE, related_name='assessment_grades')
    enrollment = models.ForeignKey('students.StudentEnrollment', null=True, blank=True, on_delete=models.SET_NULL, related_name='assessment_grades')
    score = models.DecimalField(max_digits=5, decimal_places=2)
    feedback = models.TextField(blank=True)
    is_absent = models.BooleanField(default=False)

    class Meta:
        ordering = ['assessment__title', 'student__full_name']
        unique_together = [('assessment', 'student')]

    def clean(self):
        super().clean()
        if self.assessment_id and self.student_id and self.student.tenant_id != self.assessment.tenant_id:
            raise ValidationError({'student': 'O aluno precisa pertencer ao mesmo tenant da avaliação.'})
        if self.enrollment_id and self.student_id and self.enrollment.student_id != self.student_id:
            raise ValidationError({'enrollment': 'A matrícula precisa pertencer ao aluno informado.'})
        if self.score is not None and self.score < 0:
            raise ValidationError({'score': 'A nota não pode ser menor que zero.'})
        if self.assessment_id and self.score is not None and self.score > self.assessment.max_score:
            raise ValidationError({'score': 'A nota não pode ser maior que a pontuação máxima da avaliação.'})

    def __str__(self):
        return f'{self.student} - {self.assessment} - {self.score}'

    @property
    def percentage(self):
        if not self.assessment.max_score:
            return Decimal('0')
        return (self.score / self.assessment.max_score) * Decimal('100')


class ReportCard(TimeStampedModel):
    class Status(models.TextChoices):
        DRAFT = 'DRAFT', 'Rascunho'
        PUBLISHED = 'PUBLISHED', 'Publicado'
        ARCHIVED = 'ARCHIVED', 'Arquivado'

    tenant = models.ForeignKey('saas.Tenant', on_delete=models.CASCADE, related_name='report_cards')
    school = models.ForeignKey('schools.School', on_delete=models.CASCADE, related_name='report_cards')
    academic_year = models.ForeignKey('schools.AcademicYear', on_delete=models.CASCADE, related_name='report_cards')
    term = models.ForeignKey(SchoolTerm, null=True, blank=True, on_delete=models.SET_NULL, related_name='report_cards')
    student = models.ForeignKey('students.Student', on_delete=models.CASCADE, related_name='report_cards')
    enrollment = models.ForeignKey('students.StudentEnrollment', null=True, blank=True, on_delete=models.SET_NULL, related_name='report_cards')
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.DRAFT)
    published_at = models.DateTimeField(null=True, blank=True)
    general_comments = models.TextField(blank=True)

    class Meta:
        ordering = ['student__full_name', 'academic_year__year']
        unique_together = [('academic_year', 'term', 'student')]

    def __str__(self):
        term_name = self.term.name if self.term else 'Ano letivo'
        return f'{self.student} - {self.academic_year.year} - {term_name}'

    @property
    def is_published(self):
        return self.status == self.Status.PUBLISHED

    def publish(self):
        self.status = self.Status.PUBLISHED
        if self.published_at is None:
            self.published_at = timezone.now()
        self.save(update_fields=['status', 'published_at', 'updated_at'])


class ReportCardEntry(TimeStampedModel):
    tenant = models.ForeignKey('saas.Tenant', on_delete=models.CASCADE, related_name='report_card_entries')
    report_card = models.ForeignKey(ReportCard, on_delete=models.CASCADE, related_name='entries')
    subject = models.ForeignKey('academics.Subject', on_delete=models.CASCADE, related_name='report_card_entries')
    average_score = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal('0.00'))
    absences_count = models.PositiveIntegerField(default=0)
    teacher_comments = models.TextField(blank=True)

    class Meta:
        ordering = ['report_card', 'subject__name']
        unique_together = [('report_card', 'subject')]

    def clean(self):
        super().clean()
        if self.average_score is not None and self.average_score < 0:
            raise ValidationError({'average_score': 'A média não pode ser menor que zero.'})
        if self.average_score is not None and self.average_score > 10:
            raise ValidationError({'average_score': 'A média não pode ser maior que 10.'})

    def __str__(self):
        return f'{self.report_card} - {self.subject} - {self.average_score}'

    @property
    def is_below_average(self):
        return self.average_score < Decimal('6')
