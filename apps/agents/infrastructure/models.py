from django.db import models
from apps.core.infrastructure.models import TimeStampedModel

class AgentProfile(TimeStampedModel):
    class Kind(models.TextChoices):
        LIVIA = 'livia', 'Lívia - Assistente virtual'
        ATLAS = 'atlas', 'Atlas - Prospecção'
        POLICY = 'policy', 'Policy Guard'
        CUSTOM = 'custom', 'Customizado'

    name = models.CharField(max_length=120)
    kind = models.CharField(max_length=30, choices=Kind.choices)
    purpose = models.TextField()
    instructions = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class VirtualAssistantSession(TimeStampedModel):
    agent = models.ForeignKey(AgentProfile, null=True, blank=True, on_delete=models.SET_NULL)
    customer = models.ForeignKey('customers.Customer', null=True, blank=True, on_delete=models.SET_NULL)
    channel = models.CharField(max_length=40, default='web')
    visitor_name = models.CharField(max_length=160, blank=True)
    visitor_email = models.EmailField(blank=True)
    visitor_phone = models.CharField(max_length=40, blank=True)
    summary = models.TextField(blank=True)
    status = models.CharField(max_length=30, default='open')

class VirtualAssistantMessage(TimeStampedModel):
    class Role(models.TextChoices):
        USER = 'user', 'Usuário'
        ASSISTANT = 'assistant', 'Assistente'
        SYSTEM = 'system', 'Sistema'

    session = models.ForeignKey(VirtualAssistantSession, on_delete=models.CASCADE, related_name='messages')
    role = models.CharField(max_length=20, choices=Role.choices)
    content = models.TextField()
    metadata = models.JSONField(default=dict, blank=True)

class AtlasProspect(TimeStampedModel):
    class Status(models.TextChoices):
        NEW = 'new', 'Novo'
        REVIEW = 'review', 'Revisão'
        APPROVED = 'approved', 'Aprovado'
        REJECTED = 'rejected', 'Rejeitado'
        CONTACTED = 'contacted', 'Contatado'

    company_name = models.CharField(max_length=180)
    website = models.URLField(blank=True)
    contact_name = models.CharField(max_length=160, blank=True)
    contact_email = models.EmailField(blank=True)
    phone = models.CharField(max_length=40, blank=True)
    city = models.CharField(max_length=120, blank=True)
    state = models.CharField(max_length=2, blank=True)
    source = models.CharField(max_length=160, blank=True)
    score = models.PositiveSmallIntegerField(default=0)
    status = models.CharField(max_length=30, choices=Status.choices, default=Status.NEW)
    evidence = models.JSONField(default=dict, blank=True)
    notes = models.TextField(blank=True)

class AtlasEmailDraft(TimeStampedModel):
    prospect = models.ForeignKey(AtlasProspect, on_delete=models.CASCADE, related_name='email_drafts')
    subject = models.CharField(max_length=180)
    body = models.TextField()
    to_email = models.EmailField()
    from_email = models.EmailField(blank=True)
    approved_by_human = models.BooleanField(default=False)
    sent_at = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=30, default='draft')
