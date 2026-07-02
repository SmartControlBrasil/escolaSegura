from django.db import models
from django.db.models import Q


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Guardian(TimeStampedModel):
    tenant = models.ForeignKey('saas.Tenant', on_delete=models.CASCADE, related_name='guardians')
    school = models.ForeignKey('schools.School', on_delete=models.CASCADE, related_name='guardians')
    full_name = models.CharField(max_length=180)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=32, blank=True)
    document_number = models.CharField(max_length=32, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['full_name']
        constraints = [
            models.UniqueConstraint(
                fields=['school', 'document_number'],
                condition=~Q(document_number=''),
                name='uniq_guardian_document_per_school_when_filled',
            ),
        ]

    def __str__(self):
        return self.full_name


class GuardianStudentLink(TimeStampedModel):
    class Relationship(models.TextChoices):
        MOTHER = 'MOTHER', 'Mãe'
        FATHER = 'FATHER', 'Pai'
        LEGAL_GUARDIAN = 'LEGAL_GUARDIAN', 'Responsável legal'
        FINANCIAL_RESPONSIBLE = 'FINANCIAL_RESPONSIBLE', 'Responsável financeiro'
        EMERGENCY_CONTACT = 'EMERGENCY_CONTACT', 'Contato de emergência'
        OTHER = 'OTHER', 'Outro'

    tenant = models.ForeignKey('saas.Tenant', on_delete=models.CASCADE, related_name='guardian_student_links')
    guardian = models.ForeignKey(Guardian, on_delete=models.CASCADE, related_name='student_links')
    student = models.ForeignKey('students.Student', on_delete=models.CASCADE, related_name='guardian_links')
    relationship = models.CharField(max_length=30, choices=Relationship.choices)
    can_pickup = models.BooleanField(default=False)
    can_view_financial = models.BooleanField(default=False)
    can_receive_messages = models.BooleanField(default=True)
    can_authorize_events = models.BooleanField(default=False)
    is_primary = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['guardian__full_name', 'student__full_name', 'relationship']
        unique_together = [('guardian', 'student', 'relationship')]

    def __str__(self):
        return f'{self.guardian} - {self.student} - {self.get_relationship_display()}'
