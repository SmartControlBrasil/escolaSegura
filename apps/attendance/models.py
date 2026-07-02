from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class AttendanceSession(TimeStampedModel):
    class Status(models.TextChoices):
        OPEN = 'OPEN', 'Aberta'
        CLOSED = 'CLOSED', 'Fechada'
        CANCELED = 'CANCELED', 'Cancelada'

    tenant = models.ForeignKey('saas.Tenant', on_delete=models.CASCADE, related_name='attendance_sessions')
    school = models.ForeignKey('schools.School', on_delete=models.CASCADE, related_name='attendance_sessions')
    academic_year = models.ForeignKey('schools.AcademicYear', on_delete=models.CASCADE, related_name='attendance_sessions')
    class_group = models.ForeignKey('academics.ClassGroup', on_delete=models.CASCADE, related_name='attendance_sessions')
    subject = models.ForeignKey('academics.Subject', null=True, blank=True, on_delete=models.SET_NULL, related_name='attendance_sessions')
    teacher = models.ForeignKey('academics.TeacherProfile', null=True, blank=True, on_delete=models.SET_NULL, related_name='attendance_sessions')
    session_date = models.DateField()
    session_number = models.PositiveIntegerField(default=1)
    notes = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.OPEN)

    class Meta:
        ordering = ['-session_date', 'class_group']
        unique_together = [('class_group', 'subject', 'session_date', 'session_number')]

    def __str__(self):
        return f'{self.class_group} - {self.session_date} - chamada {self.session_number}'

    @property
    def is_editable(self):
        return self.status == self.Status.OPEN


class AttendanceRecord(TimeStampedModel):
    class Status(models.TextChoices):
        PRESENT = 'PRESENT', 'Presente'
        ABSENT = 'ABSENT', 'Ausente'
        LATE = 'LATE', 'Atrasado'
        JUSTIFIED = 'JUSTIFIED', 'Justificado'
        REMOTE = 'REMOTE', 'Remoto'

    tenant = models.ForeignKey('saas.Tenant', on_delete=models.CASCADE, related_name='attendance_records')
    session = models.ForeignKey(AttendanceSession, on_delete=models.CASCADE, related_name='records')
    student = models.ForeignKey('students.Student', on_delete=models.CASCADE, related_name='attendance_records')
    enrollment = models.ForeignKey('students.StudentEnrollment', null=True, blank=True, on_delete=models.SET_NULL, related_name='attendance_records')
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PRESENT)
    arrival_time = models.TimeField(null=True, blank=True)
    notes = models.TextField(blank=True)
    marked_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL, related_name='marked_attendance_records')
    marked_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['session', 'student__full_name']
        unique_together = [('session', 'student')]

    def clean(self):
        super().clean()
        if self.session_id and self.student_id and self.student.tenant_id != self.session.tenant_id:
            raise ValidationError({'student': 'O aluno precisa pertencer ao mesmo tenant da sessão.'})
        if self.enrollment_id and self.student_id and self.enrollment.student_id != self.student_id:
            raise ValidationError({'enrollment': 'A matrícula precisa pertencer ao aluno informado.'})

    def __str__(self):
        return f'{self.student} - {self.session} - {self.get_status_display()}'

    @property
    def is_absence(self):
        return self.status == self.Status.ABSENT

    @property
    def requires_justification(self):
        return self.status in {self.Status.ABSENT, self.Status.LATE}


class AbsenceJustification(TimeStampedModel):
    class Status(models.TextChoices):
        PENDING = 'PENDING', 'Pendente'
        APPROVED = 'APPROVED', 'Aprovada'
        REJECTED = 'REJECTED', 'Rejeitada'

    tenant = models.ForeignKey('saas.Tenant', on_delete=models.CASCADE, related_name='absence_justifications')
    record = models.OneToOneField(AttendanceRecord, on_delete=models.CASCADE, related_name='justification')
    submitted_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL, related_name='submitted_absence_justifications')
    reason = models.TextField()
    attachment = models.FileField(upload_to='attendance/justifications/%Y/%m/', null=True, blank=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    reviewed_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL, related_name='reviewed_absence_justifications')
    reviewed_at = models.DateTimeField(null=True, blank=True)
    review_notes = models.TextField(blank=True)

    class Meta:
        ordering = ['-created_at']

    def clean(self):
        super().clean()
        if self.record_id and self.record.tenant_id != self.tenant_id:
            raise ValidationError({'record': 'O registro precisa pertencer ao mesmo tenant da justificativa.'})

    def __str__(self):
        return f'{self.record.student} - {self.get_status_display()}'

    def approve(self, user=None, notes=''):
        self.status = self.Status.APPROVED
        if user is not None:
            self.reviewed_by = user
        self.reviewed_at = timezone.now()
        self.review_notes = notes
        self.save(update_fields=['status', 'reviewed_by', 'reviewed_at', 'review_notes', 'updated_at'])
        if self.record.status == AttendanceRecord.Status.ABSENT:
            self.record.status = AttendanceRecord.Status.JUSTIFIED
            self.record.save(update_fields=['status', 'updated_at'])

    def reject(self, user=None, notes=''):
        self.status = self.Status.REJECTED
        if user is not None:
            self.reviewed_by = user
        self.reviewed_at = timezone.now()
        self.review_notes = notes
        self.save(update_fields=['status', 'reviewed_by', 'reviewed_at', 'review_notes', 'updated_at'])
