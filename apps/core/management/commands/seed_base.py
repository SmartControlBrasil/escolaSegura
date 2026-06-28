from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from rest_framework.authtoken.models import Token

from apps.agents.infrastructure.models import AgentProfile
from apps.catalog.infrastructure.models import ProductCategory
from apps.core.infrastructure.models import Organization, SystemSetting
from apps.inventory.infrastructure.models import StockLocation
from apps.policy_guard.infrastructure.models import DataProcessingRecord

class Command(BaseCommand):
    help = 'Cria dados iniciais seguros para operação da base.'

    def handle(self, *args, **options):
        org, _ = Organization.objects.get_or_create(
            name='Smart System Base',
            defaults={'legal_name': 'Smart System Base', 'document': '00000000000000'},
        )
        StockLocation.objects.get_or_create(organization=org, code='MAIN', defaults={'name':'Almoxarifado Principal'})
        ProductCategory.objects.get_or_create(organization=org, slug='geral', defaults={'name':'Geral'})
        SystemSetting.objects.get_or_create(key='security.policy', defaults={'value': {'lgpd_by_design': True}, 'description':'Política padrão de segurança e LGPD'})
        DataProcessingRecord.objects.get_or_create(
            process_name='Cadastro de clientes',
            defaults={'legal_basis': 'execucao_contrato', 'purpose': 'Gestão comercial e operacional', 'data_categories': ['identificação','contato']},
        )
        AgentProfile.objects.get_or_create(kind='livia', name='Lívia', defaults={'purpose':'Assistente virtual consultiva para atendimento e qualificação.'})
        AgentProfile.objects.get_or_create(kind='atlas', name='Atlas', defaults={'purpose':'Agente de prospecção com revisão humana antes de outreach.'})
        AgentProfile.objects.get_or_create(kind='policy', name='Policy Guard', defaults={'purpose':'Agente de LGPD e segurança da informação.'})
        User = get_user_model()
        user, created = User.objects.get_or_create(username='admin', defaults={'email':'admin@smart-system.local','is_staff':True,'is_superuser':True,'role':'owner','organization':org})
        if created:
            user.set_password('admin123')
            user.save()
        Token.objects.get_or_create(user=user)
        self.stdout.write(self.style.SUCCESS('Base inicial criada. Usuário: admin / Senha: admin123'))
