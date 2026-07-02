from decimal import Decimal

from django.core.management.base import BaseCommand

from apps.saas.models import PlanFeature, SubscriptionPlan


FEATURE_NAMES = {
    'students': 'Alunos',
    'guardians': 'Responsáveis',
    'classes': 'Turmas',
    'attendance': 'Frequência',
    'communication': 'Comunicação',
    'parent_portal': 'Portal dos pais',
    'assessments': 'Avaliações',
    'report_cards': 'Boletins',
    'documents': 'Documentos',
    'school_finance': 'Financeiro escolar',
    'billing': 'Cobranças',
    'whatsapp': 'WhatsApp',
    'ai_assistant': 'Assistente IA',
    'pedagogical_alerts': 'Alertas pedagógicos',
    'api': 'API',
}


PLANS = [
    {
        'slug': 'essencial',
        'name': 'Essencial',
        'description': 'Fundação operacional para escolas em início de organização digital.',
        'monthly_price': Decimal('197.00'),
        'annual_price': Decimal('1970.00'),
        'max_students': 100,
        'max_users': 20,
        'display_order': 1,
        'features': ['students', 'guardians', 'classes', 'attendance', 'communication', 'parent_portal'],
    },
    {
        'slug': 'academico',
        'name': 'Acadêmico',
        'description': 'Gestão acadêmica com avaliações, boletins e documentos.',
        'monthly_price': Decimal('347.00'),
        'annual_price': Decimal('3470.00'),
        'max_students': 300,
        'max_users': 60,
        'has_academics': True,
        'has_documents': True,
        'display_order': 2,
        'features': [
            'students', 'guardians', 'classes', 'attendance', 'communication', 'parent_portal',
            'assessments', 'report_cards', 'documents',
        ],
    },
    {
        'slug': 'gestao',
        'name': 'Gestão',
        'description': 'Gestão escolar ampliada com financeiro, cobranças e WhatsApp.',
        'monthly_price': Decimal('597.00'),
        'annual_price': Decimal('5970.00'),
        'max_students': 700,
        'max_users': 120,
        'has_academics': True,
        'has_finance': True,
        'has_documents': True,
        'has_whatsapp': True,
        'display_order': 3,
        'features': [
            'students', 'guardians', 'classes', 'attendance', 'communication', 'parent_portal',
            'assessments', 'report_cards', 'documents', 'school_finance', 'billing', 'whatsapp',
        ],
    },
    {
        'slug': 'ia',
        'name': 'IA',
        'description': 'Suíte completa com IA, alertas pedagógicos e API.',
        'monthly_price': Decimal('897.00'),
        'annual_price': Decimal('8970.00'),
        'max_students': 1200,
        'max_users': 250,
        'has_academics': True,
        'has_finance': True,
        'has_documents': True,
        'has_ai': True,
        'has_whatsapp': True,
        'has_api': True,
        'display_order': 4,
        'features': [
            'students', 'guardians', 'classes', 'attendance', 'communication', 'parent_portal',
            'assessments', 'report_cards', 'documents', 'school_finance', 'billing', 'whatsapp',
            'ai_assistant', 'pedagogical_alerts', 'api',
        ],
    },
]


class Command(BaseCommand):
    help = 'Cria ou atualiza os planos SaaS iniciais do EscolaSegura.'

    def handle(self, *args, **options):
        for source in PLANS:
            plan_data = source.copy()
            feature_codes = plan_data.pop('features')
            plan, _created = SubscriptionPlan.objects.update_or_create(
                slug=plan_data['slug'],
                defaults=plan_data,
            )
            for code in feature_codes:
                PlanFeature.objects.update_or_create(
                    plan=plan,
                    code=code,
                    defaults={
                        'name': FEATURE_NAMES[code],
                        'description': '',
                        'is_enabled': True,
                    },
                )
            plan.features.exclude(code__in=feature_codes).update(is_enabled=False)

        self.stdout.write(self.style.SUCCESS('Planos EscolaSegura criados/atualizados com sucesso.'))
