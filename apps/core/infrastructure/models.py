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

    @property
    def company_profile(self):
        try:
            if hasattr(self, 'profile') and self.profile:
                return self.profile
        except Exception:
            pass
        return FallbackCompanyProfile(self)

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

class Supplier(TimeStampedModel):
    organization = models.ForeignKey(Organization, null=True, blank=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=180)
    cnpj = models.CharField(max_length=32, blank=True)
    phone = models.CharField(max_length=32, blank=True)
    email = models.EmailField(blank=True)
    city = models.CharField(max_length=120, blank=True)
    address = models.TextField(blank=True)
    category = models.CharField(max_length=120, blank=True)
    is_active = models.BooleanField(default=True)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Vehicle(TimeStampedModel):
    organization = models.ForeignKey(Organization, null=True, blank=True, on_delete=models.SET_NULL)
    plate = models.CharField(max_length=20)
    model = models.CharField(max_length=120, blank=True)
    brand = models.CharField(max_length=120, blank=True)
    year = models.IntegerField(null=True, blank=True)
    driver = models.ForeignKey('accounts.User', null=True, blank=True, on_delete=models.SET_NULL)
    status = models.CharField(max_length=50, default='active')
    usage = models.CharField(max_length=120, blank=True)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ['plate']

    def __str__(self):
        return f'{self.plate} - {self.model}'


class FallbackCompanyProfile:
    def __init__(self, organization):
        self.organization = organization
        self.trade_name = organization.name or "EscolaSegura"
        self.legal_name = organization.legal_name or "EscolaSegura LTDA"
        self.cnpj = organization.document or "12.345.678/0001-99"
        self.phone = organization.phone or "(11) 4142-1413"
        self.whatsapp = "(11) 99999-8888"
        self.email = organization.email or "contato@escolasegura360.com.br"
        self.website = "https://escolasegura360.com.br"
        self.address = "Av. Exemplo Comercial, 1000 - Centro"
        self.city = "São Paulo"
        self.state = "SP"
        self.business_hours = "Segunda a Sexta: 08:00 às 18:00"
        self.slogan = "Gestão escolar conectada e segura"
        self.footer_text = "Documento gerado por EscolaSegura - Todos os direitos reservados."
        self.default_terms = "Condições comerciais definidas pela escola contratante."
        self.default_estimate_validity = 15
        self.privacy_policy = "Esta é a política de privacidade da EscolaSegura."
        self.terms_of_use = "Estes são os termos de uso do sistema da EscolaSegura."
        self.logo = None
        self.is_active = True


class CompanyProfile(TimeStampedModel):
    organization = models.OneToOneField(Organization, on_delete=models.CASCADE, related_name='profile')
    trade_name = models.CharField(max_length=180, verbose_name="Nome Fantasia")
    legal_name = models.CharField(max_length=220, blank=True, verbose_name="Razão Social")
    cnpj = models.CharField(max_length=32, blank=True, verbose_name="CNPJ")
    phone = models.CharField(max_length=32, blank=True, verbose_name="Telefone")
    whatsapp = models.CharField(max_length=32, blank=True, verbose_name="WhatsApp")
    email = models.EmailField(blank=True, verbose_name="E-mail Comercial")
    website = models.URLField(blank=True, verbose_name="Site")
    address = models.TextField(blank=True, verbose_name="Endereço Completo")
    city = models.CharField(max_length=120, blank=True, verbose_name="Cidade")
    state = models.CharField(max_length=2, blank=True, verbose_name="UF")
    business_hours = models.CharField(max_length=240, blank=True, verbose_name="Horário de Atendimento")
    slogan = models.CharField(max_length=240, blank=True, verbose_name="Slogan")
    footer_text = models.TextField(blank=True, verbose_name="Texto Padrão de Rodapé")
    default_terms = models.TextField(blank=True, verbose_name="Condições Comerciais Padrão")
    default_estimate_validity = models.PositiveIntegerField(default=7, verbose_name="Prazo Padrão de Validade do Orçamento")
    privacy_policy = models.TextField(blank=True, verbose_name="Política de Privacidade")
    terms_of_use = models.TextField(blank=True, verbose_name="Termos de Uso")
    logo = models.ImageField(upload_to='company/logos/', null=True, blank=True, verbose_name="Logo")
    is_active = models.BooleanField(default=True, verbose_name="Status Ativo")

    class Meta:
        verbose_name = "Perfil da Empresa"
        verbose_name_plural = "Perfis de Empresa"

    def __str__(self):
        return self.trade_name or self.organization.name
