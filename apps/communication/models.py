from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Announcement(TimeStampedModel):
    class Priority(models.TextChoices):
        LOW = 'LOW', 'Baixa'
        NORMAL = 'NORMAL', 'Normal'
        HIGH = 'HIGH', 'Alta'
        URGENT = 'URGENT', 'Urgente'

    class Status(models.TextChoices):
        DRAFT = 'DRAFT', 'Rascunho'
        PUBLISHED = 'PUBLISHED', 'Publicado'
        ARCHIVED = 'ARCHIVED', 'Arquivado'

    tenant = models.ForeignKey('saas.Tenant', on_delete=models.CASCADE, related_name='announcements')
    school = models.ForeignKey('schools.School', on_delete=models.CASCADE, related_name='announcements')
    unit = models.ForeignKey('schools.SchoolUnit', null=True, blank=True, on_delete=models.SET_NULL, related_name='announcements')
    academic_year = models.ForeignKey('schools.AcademicYear', null=True, blank=True, on_delete=models.SET_NULL, related_name='announcements')
    title = models.CharField(max_length=180)
    body = models.TextField()
    priority = models.CharField(max_length=20, choices=Priority.choices, default=Priority.NORMAL)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.DRAFT)
    published_at = models.DateTimeField(null=True, blank=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL, related_name='created_announcements')

    class Meta:
        ordering = ['-published_at', '-created_at']

    def __str__(self):
        return self.title

    @property
    def is_published(self):
        return self.status == self.Status.PUBLISHED

    def publish(self, user=None):
        self.status = self.Status.PUBLISHED
        if self.published_at is None:
            self.published_at = timezone.now()
        if user is not None and self.created_by_id is None:
            self.created_by = user
        self.save(update_fields=['status', 'published_at', 'created_by', 'updated_at'])


class AnnouncementAudience(TimeStampedModel):
    class AudienceType(models.TextChoices):
        ALL_SCHOOL = 'ALL_SCHOOL', 'Escola inteira'
        UNIT = 'UNIT', 'Unidade'
        CLASS_GROUP = 'CLASS_GROUP', 'Turma'
        STUDENT = 'STUDENT', 'Aluno específico'
        GUARDIAN = 'GUARDIAN', 'Responsável específico'

    tenant = models.ForeignKey('saas.Tenant', on_delete=models.CASCADE, related_name='announcement_audiences')
    announcement = models.ForeignKey(Announcement, on_delete=models.CASCADE, related_name='audiences')
    audience_type = models.CharField(max_length=30, choices=AudienceType.choices)
    unit = models.ForeignKey('schools.SchoolUnit', null=True, blank=True, on_delete=models.CASCADE, related_name='announcement_audiences')
    class_group = models.ForeignKey('academics.ClassGroup', null=True, blank=True, on_delete=models.CASCADE, related_name='announcement_audiences')
    student = models.ForeignKey('students.Student', null=True, blank=True, on_delete=models.CASCADE, related_name='announcement_audiences')
    guardian = models.ForeignKey('guardians.Guardian', null=True, blank=True, on_delete=models.CASCADE, related_name='announcement_audiences')

    class Meta:
        ordering = ['announcement__title', 'audience_type']

    def clean(self):
        super().clean()
        required_by_type = {
            self.AudienceType.UNIT: ('unit', self.unit_id),
            self.AudienceType.CLASS_GROUP: ('class_group', self.class_group_id),
            self.AudienceType.STUDENT: ('student', self.student_id),
            self.AudienceType.GUARDIAN: ('guardian', self.guardian_id),
        }
        required = required_by_type.get(self.audience_type)
        if required and not required[1]:
            raise ValidationError({required[0]: 'Este alvo é obrigatório para o tipo de público selecionado.'})

    def __str__(self):
        return f'{self.announcement} - {self.get_audience_type_display()}'


class AnnouncementReadReceipt(TimeStampedModel):
    class Channel(models.TextChoices):
        PORTAL = 'PORTAL', 'Portal'
        APP = 'APP', 'App'
        EMAIL = 'EMAIL', 'E-mail'
        WHATSAPP = 'WHATSAPP', 'WhatsApp'

    tenant = models.ForeignKey('saas.Tenant', on_delete=models.CASCADE, related_name='announcement_read_receipts')
    announcement = models.ForeignKey(Announcement, on_delete=models.CASCADE, related_name='read_receipts')
    guardian = models.ForeignKey('guardians.Guardian', null=True, blank=True, on_delete=models.CASCADE, related_name='announcement_read_receipts')
    student = models.ForeignKey('students.Student', null=True, blank=True, on_delete=models.CASCADE, related_name='announcement_read_receipts')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.CASCADE, related_name='announcement_read_receipts')
    read_at = models.DateTimeField(default=timezone.now)
    channel = models.CharField(max_length=20, choices=Channel.choices, default=Channel.PORTAL)

    class Meta:
        ordering = ['-read_at']
        unique_together = [('announcement', 'guardian', 'student', 'user')]

    def clean(self):
        super().clean()
        if not (self.guardian_id or self.student_id or self.user_id):
            raise ValidationError('Informe ao menos um leitor: responsável, aluno ou usuário.')

    def __str__(self):
        reader = self.guardian or self.student or self.user or 'sem leitor'
        return f'{self.announcement} - {reader}'


class MessageThread(TimeStampedModel):
    class Status(models.TextChoices):
        OPEN = 'OPEN', 'Aberta'
        PENDING = 'PENDING', 'Pendente'
        CLOSED = 'CLOSED', 'Encerrada'

    class Priority(models.TextChoices):
        LOW = 'LOW', 'Baixa'
        NORMAL = 'NORMAL', 'Normal'
        HIGH = 'HIGH', 'Alta'
        URGENT = 'URGENT', 'Urgente'

    tenant = models.ForeignKey('saas.Tenant', on_delete=models.CASCADE, related_name='message_threads')
    school = models.ForeignKey('schools.School', on_delete=models.CASCADE, related_name='message_threads')
    student = models.ForeignKey('students.Student', null=True, blank=True, on_delete=models.SET_NULL, related_name='message_threads')
    guardian = models.ForeignKey('guardians.Guardian', null=True, blank=True, on_delete=models.SET_NULL, related_name='message_threads')
    subject = models.CharField(max_length=180)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.OPEN)
    priority = models.CharField(max_length=20, choices=Priority.choices, default=Priority.NORMAL)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL, related_name='created_message_threads')
    closed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.subject

    @property
    def is_open(self):
        return self.status != self.Status.CLOSED

    def close(self):
        self.status = self.Status.CLOSED
        self.closed_at = timezone.now()
        self.save(update_fields=['status', 'closed_at', 'updated_at'])


class Message(TimeStampedModel):
    tenant = models.ForeignKey('saas.Tenant', on_delete=models.CASCADE, related_name='messages')
    thread = models.ForeignKey(MessageThread, on_delete=models.CASCADE, related_name='messages')
    sender_user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL, related_name='sent_school_messages')
    sender_guardian = models.ForeignKey('guardians.Guardian', null=True, blank=True, on_delete=models.SET_NULL, related_name='sent_messages')
    sender_student = models.ForeignKey('students.Student', null=True, blank=True, on_delete=models.SET_NULL, related_name='sent_messages')
    body = models.TextField()
    sent_at = models.DateTimeField(default=timezone.now)
    read_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['sent_at']

    def clean(self):
        super().clean()
        if not (self.sender_user_id or self.sender_guardian_id or self.sender_student_id):
            raise ValidationError('Informe ao menos um remetente.')

    def __str__(self):
        return f'{self.thread} - {self.sent_at}'

    @property
    def is_read(self):
        return bool(self.read_at)

    def mark_read(self):
        if self.read_at is None:
            self.read_at = timezone.now()
            self.save(update_fields=['read_at', 'updated_at'])


class AuthorizationRequest(TimeStampedModel):
    class RequestType(models.TextChoices):
        EVENT = 'EVENT', 'Evento'
        FIELD_TRIP = 'FIELD_TRIP', 'Passeio'
        IMAGE_USE = 'IMAGE_USE', 'Uso de imagem'
        PICKUP = 'PICKUP', 'Retirada'
        OTHER = 'OTHER', 'Outro'

    class Status(models.TextChoices):
        OPEN = 'OPEN', 'Aberta'
        CLOSED = 'CLOSED', 'Encerrada'
        CANCELED = 'CANCELED', 'Cancelada'

    tenant = models.ForeignKey('saas.Tenant', on_delete=models.CASCADE, related_name='authorization_requests')
    school = models.ForeignKey('schools.School', on_delete=models.CASCADE, related_name='authorization_requests')
    student = models.ForeignKey('students.Student', on_delete=models.CASCADE, related_name='authorization_requests')
    title = models.CharField(max_length=180)
    description = models.TextField()
    request_type = models.CharField(max_length=20, choices=RequestType.choices, default=RequestType.OTHER)
    due_at = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.OPEN)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL, related_name='created_authorization_requests')

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.title} - {self.student}'

    @property
    def is_open(self):
        return self.status == self.Status.OPEN


class AuthorizationResponse(TimeStampedModel):
    class Response(models.TextChoices):
        APPROVED = 'APPROVED', 'Autorizado'
        REJECTED = 'REJECTED', 'Não autorizado'

    tenant = models.ForeignKey('saas.Tenant', on_delete=models.CASCADE, related_name='authorization_responses')
    request = models.ForeignKey(AuthorizationRequest, on_delete=models.CASCADE, related_name='responses')
    guardian = models.ForeignKey('guardians.Guardian', on_delete=models.CASCADE, related_name='authorization_responses')
    response = models.CharField(max_length=20, choices=Response.choices)
    notes = models.TextField(blank=True)
    responded_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-responded_at']
        unique_together = [('request', 'guardian')]

    def clean(self):
        super().clean()
        if self.request_id and self.guardian_id:
            from apps.guardians.models import GuardianStudentLink

            can_authorize = GuardianStudentLink.objects.filter(
                tenant=self.tenant,
                guardian=self.guardian,
                student=self.request.student,
                is_active=True,
                can_authorize_events=True,
            ).exists()
            if not can_authorize:
                raise ValidationError({'guardian': 'O responsável não está autorizado a responder esta solicitação.'})

    def __str__(self):
        return f'{self.request} - {self.guardian} - {self.get_response_display()}'
