from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Q
from django.utils import timezone


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Student(TimeStampedModel):
    class Status(models.TextChoices):
        ACTIVE = 'ACTIVE', 'Ativo'
        TRANSFERRED = 'TRANSFERRED', 'Transferido'
        SUSPENDED = 'SUSPENDED', 'Suspenso'
        GRADUATED = 'GRADUATED', 'Formado'
        INACTIVE = 'INACTIVE', 'Inativo'

    tenant = models.ForeignKey('saas.Tenant', on_delete=models.CASCADE, related_name='students')
    school = models.ForeignKey('schools.School', on_delete=models.CASCADE, related_name='students')
    full_name = models.CharField(max_length=180)
    preferred_name = models.CharField(max_length=120, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    document_number = models.CharField(max_length=32, blank=True)
    student_code = models.CharField(max_length=40, blank=True)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=32, blank=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.ACTIVE)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['full_name']
        constraints = [
            models.UniqueConstraint(
                fields=['school', 'student_code'],
                condition=~Q(student_code=''),
                name='uniq_student_code_per_school_when_filled',
            ),
        ]

    def __str__(self):
        return self.full_name


class StudentEnrollment(TimeStampedModel):
    class Status(models.TextChoices):
        ACTIVE = 'ACTIVE', 'Ativa'
        PENDING = 'PENDING', 'Pendente'
        CANCELED = 'CANCELED', 'Cancelada'
        TRANSFERRED = 'TRANSFERRED', 'Transferida'
        COMPLETED = 'COMPLETED', 'Concluída'

    tenant = models.ForeignKey('saas.Tenant', on_delete=models.CASCADE, related_name='student_enrollments')
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='enrollments')
    school = models.ForeignKey('schools.School', on_delete=models.CASCADE, related_name='student_enrollments')
    academic_year = models.ForeignKey('schools.AcademicYear', on_delete=models.CASCADE, related_name='student_enrollments')
    class_group = models.ForeignKey('academics.ClassGroup', on_delete=models.PROTECT, related_name='student_enrollments')
    enrollment_number = models.CharField(max_length=40, blank=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.ACTIVE)
    enrolled_at = models.DateField(default=timezone.localdate)
    exited_at = models.DateField(null=True, blank=True)

    class Meta:
        ordering = ['student__full_name', '-enrolled_at']
        constraints = [
            models.UniqueConstraint(
                fields=['school', 'enrollment_number'],
                condition=~Q(enrollment_number=''),
                name='uniq_enrollment_number_per_school_when_filled',
            ),
        ]

    def clean(self):
        super().clean()
        if self.status == self.Status.ACTIVE and self.student_id and self.academic_year_id:
            duplicate = StudentEnrollment.objects.filter(
                student=self.student,
                academic_year=self.academic_year,
                status=self.Status.ACTIVE,
            ).exclude(pk=self.pk)
            if duplicate.exists():
                raise ValidationError('O aluno já possui matrícula ativa neste ano letivo.')

    def __str__(self):
        return f'{self.student} - {self.academic_year.year} - {self.class_group}'
