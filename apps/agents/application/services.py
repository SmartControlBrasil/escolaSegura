from django.conf import settings
from django.core.mail import send_mail
from django.utils import timezone

class LiviaAssistantService:
    """Serviço determinístico inicial. A troca por LLM entra por adapter externo."""
    REQUIRED_FIELDS = ['visitor_name', 'visitor_phone', 'visitor_email']

    @staticmethod
    def next_question(session):
        if not session.visitor_name:
            return 'Claro. Para eu registrar corretamente, qual é o seu nome?'
        if not session.visitor_phone:
            return 'Perfeito. Qual telefone ou WhatsApp para contato?'
        if not session.visitor_email:
            return 'Ótimo. Qual e-mail podemos usar para retorno?'
        return 'Obrigado. Já tenho os dados principais. Pode me contar mais detalhes da necessidade?'

class AtlasProspectorService:
    @staticmethod
    def create_email_draft(prospect, subject, body, from_email=None):
        from apps.agents.infrastructure.models import AtlasEmailDraft
        return AtlasEmailDraft.objects.create(
            prospect=prospect,
            subject=subject,
            body=body,
            to_email=prospect.contact_email,
            from_email=from_email or settings.ATLAS_DEFAULT_FROM_EMAIL,
        )

    @staticmethod
    def send_approved_draft(draft):
        if not draft.approved_by_human:
            raise ValueError('Envio bloqueado: draft precisa de aprovação humana.')
        if settings.AGENTS_EMAIL_DRY_RUN:
            draft.status = 'dry_run'
            draft.save(update_fields=['status','updated_at'])
            return False
        send_mail(draft.subject, draft.body, draft.from_email, [draft.to_email])
        draft.sent_at = timezone.now()
        draft.status = 'sent'
        draft.save(update_fields=['sent_at','status','updated_at'])
        return True
