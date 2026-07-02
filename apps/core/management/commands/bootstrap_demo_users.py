import os
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from apps.core.infrastructure.models import Organization

class Command(BaseCommand):
    help = 'Cria e atualiza com segurança os grupos de acesso e os usuários demo/superuser com base em variáveis de ambiente.'

    def handle(self, *args, **options):
        # 1. Validar variáveis do .env
        su_user = os.getenv('DJANGO_SUPERUSER_USERNAME')
        su_email = os.getenv('DJANGO_SUPERUSER_EMAIL')
        su_pass = os.getenv('DJANGO_SUPERUSER_PASSWORD')
        
        demo_user = os.getenv('DEMO_OWNER_USERNAME')
        demo_email = os.getenv('DEMO_OWNER_EMAIL')
        demo_pass = os.getenv('DEMO_OWNER_PASSWORD')

        if not su_pass:
            raise CommandError("A variável de ambiente DJANGO_SUPERUSER_PASSWORD não está definida no arquivo .env!")
        if not demo_pass:
            raise CommandError("A variável de ambiente DEMO_OWNER_PASSWORD não está definida no arquivo .env!")
        
        User = get_user_model()
        
        # 2. Criar Grupos Iniciais se não existirem
        group_names = [
            'Proprietário',
            'Comercial',
            'Técnico',
            'Financeiro',
            'Admin Técnico'
        ]
        groups = {}
        for name in group_names:
            group, created = Group.objects.get_or_create(name=name)
            groups[name] = group
            if created:
                self.stdout.write(f"Grupo '{name}' criado com sucesso.")

        # Obter ou criar organização padrão
        org, _ = Organization.objects.get_or_create(
            name='EscolaSegura',
            defaults={
                'legal_name': 'EscolaSegura LTDA',
                'document': '12345678000199',
                'email': 'contato@escolasegura360.com.br',
                'phone': '(11) 4142-1413',
            }
        )

        # 3. Criar / Atualizar Superuser
        superuser_obj, su_created = User.objects.get_or_create(
            username=su_user or 'admin',
            defaults={
                'email': su_email or 'admin@escola_segura.local',
                'is_staff': True,
                'is_superuser': True,
                'role': 'owner',
                'organization': org
            }
        )
        superuser_obj.set_password(su_pass)
        superuser_obj.is_staff = True
        superuser_obj.is_superuser = True
        superuser_obj.is_active = True
        superuser_obj.save()
        
        superuser_obj.groups.add(groups['Admin Técnico'])
        
        self.stdout.write(self.style.SUCCESS(
            f"Superusuário '{superuser_obj.username}' {'criado' if su_created else 'atualizado'} e associado ao grupo 'Admin Técnico'."
        ))

        # 4. Criar / Atualizar Demo Owner
        demo_obj, demo_created = User.objects.get_or_create(
            username=demo_user or 'fabrizio',
            defaults={
                'email': demo_email or 'contato@escolasegura360.com.br',
                'is_staff': False,
                'is_superuser': False,
                'role': 'owner',
                'organization': org
            }
        )
        demo_obj.set_password(demo_pass)
        demo_obj.is_active = True
        demo_obj.save()
        
        demo_obj.groups.add(groups['Proprietário'])
        
        self.stdout.write(self.style.SUCCESS(
            f"Usuário demonstrativo '{demo_obj.username}' {'criado' if demo_created else 'atualizado'} e associado ao grupo 'Proprietário'."
        ))
