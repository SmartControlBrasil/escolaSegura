import random
from decimal import Decimal
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils import timezone

from apps.core.infrastructure.models import Organization
from apps.customers.infrastructure.models import Customer, CustomerAddress, CustomerContact
from apps.catalog.infrastructure.models import ProductCategory, Product
from apps.estimates.infrastructure.models import Estimate, EstimateLine, EstimateMeasurement
from apps.service_reports.infrastructure.models import ServiceReport, ServiceReportItem

class Command(BaseCommand):
    help = 'Popula a base com dados demonstrativos para a Marmoraria Santander / Marmoraria360.'

    def handle(self, *args, **options):
        # 1. Obter ou Criar Organização
        org, _ = Organization.objects.get_or_create(
            name='Marmoraria Santander',
            defaults={
                'legal_name': 'Marmoraria Santander LTDA',
                'document': '12345678000199',
                'email': 'comercial@santandermarmoraria.com.br',
                'phone': '(11) 4142-1413',
            }
        )

        User = get_user_model()
        admin_user = User.objects.filter(is_superuser=True).first()
        if not admin_user:
            admin_user, _ = User.objects.get_or_create(
                username='admin',
                defaults={
                    'email': 'admin@smart-system.local',
                    'is_staff': True,
                    'is_superuser': True,
                    'role': 'owner',
                    'organization': org
                }
            )
            admin_user.set_password('admin123')
            admin_user.save()

        # 2. Criar Clientes de Demonstração
        clients_data = [
            {'name': 'Carlos Silva', 'type': 'person', 'email': 'carlos@email.com', 'phone': '(11) 98888-7777', 'city': 'São Paulo', 'state': 'SP'},
            {'name': 'Ana Souza', 'type': 'person', 'email': 'ana.souza@email.com', 'phone': '(11) 97777-6666', 'city': 'Santo André', 'state': 'SP'},
            {'name': 'Construtora Alfa LTDA', 'type': 'company', 'email': 'contato@construtoraalfa.com.br', 'phone': '(11) 4004-1234', 'city': 'São Bernardo do Campo', 'state': 'SP'},
            {'name': 'Juliana M. Arquitetura', 'type': 'company', 'email': 'juliana@jm-arquitetura.com', 'phone': '(11) 96666-5555', 'city': 'São Paulo', 'state': 'SP'},
        ]

        customers = []
        for cdata in clients_data:
            cust, created = Customer.objects.get_or_create(
                organization=org,
                name=cdata['name'],
                defaults={
                    'type': cdata['type'],
                    'email': cdata['email'],
                    'phone': cdata['phone'],
                    'city': cdata['city'],
                    'state': cdata['state'],
                    'status': 'active',
                    'notes': 'Cliente de demonstração importado pelo seed.'
                }
            )
            customers.append(cust)
            if created:
                # Endereço
                CustomerAddress.objects.create(
                    customer=cust,
                    street='Av. Paulista',
                    number=str(random.randint(100, 2000)),
                    complement='Apto 42' if cdata['type'] == 'person' else 'Conjunto 101',
                    district='Bela Vista',
                    city=cdata['city'],
                    state=cdata['state'],
                    zipcode='01311-000'
                )
                # Contato
                CustomerContact.objects.create(
                    customer=cust,
                    name=f"Contato {cdata['name']}",
                    role='Representante' if cdata['type'] == 'company' else 'Principal',
                    email=cdata['email'],
                    phone=cdata['phone'],
                    is_primary=True
                )

        # 3. Categorias de Materiais
        material_categories = ['Mármore', 'Granito', 'Quartzo', 'Silestone']
        categories = {}
        for cat_name in material_categories:
            slug = cat_name.lower().replace('á', 'a')
            cat, _ = ProductCategory.objects.get_or_create(
                organization=org,
                slug=slug,
                defaults={'name': cat_name, 'description': f'Materiais da categoria {cat_name}'}
            )
            categories[cat_name] = cat

        # 4. Criar Materiais (Produtos)
        materials_data = [
            ('Mármore', 'Mármore Carrara', 'MAR-CAR', 850.00, 450.00),
            ('Mármore', 'Mármore Nero Marquina', 'MAR-NER', 920.00, 500.00),
            ('Granito', 'Granito Preto São Gabriel', 'GRA-PSG', 380.00, 180.00),
            ('Granito', 'Granito Cinza Corumbá', 'GRA-COR', 250.00, 100.00),
            ('Quartzo', 'Quartzo Branco Estelar', 'QUA-EST', 1200.00, 600.00),
            ('Silestone', 'Silestone Cinza Expo', 'SIL-EXP', 1400.00, 750.00),
        ]

        materials = []
        for cat_name, name, sku, sale, cost in materials_data:
            prod, _ = Product.objects.get_or_create(
                organization=org,
                sku=sku,
                defaults={
                    'category': categories[cat_name],
                    'name': name,
                    'type': 'product',
                    'unit': 'm²',
                    'sale_price': Decimal(sale),
                    'cost_price': Decimal(cost),
                    'is_active': True,
                    'description': f'Chapa de {name} de alta qualidade.'
                }
            )
            materials.append(prod)

        # 5. Criar Serviços
        services_data = [
            ('Instalação de Bancada', 'SER-BAN', 250.00),
            ('Instalação de Pia', 'SER-PIA', 180.00),
            ('Revestimento de Escada', 'SER-ESC', 350.00),
            ('Colocação de Soleira', 'SER-SOL', 50.00),
            ('Instalação de Nicho', 'SER-NIC', 120.00),
            ('Montagem de Lavatório', 'SER-LAV', 200.00),
            ('Varanda Gourmet sob medida', 'SER-VGO', 400.00),
        ]

        services = []
        for name, sku, price in services_data:
            prod, _ = Product.objects.get_or_create(
                organization=org,
                sku=sku,
                defaults={
                    'name': name,
                    'type': 'service',
                    'unit': 'un',
                    'sale_price': Decimal(price),
                    'cost_price': Decimal(price * 0.4),
                    'is_active': True,
                    'description': f'Serviço profissional de {name}.'
                }
            )
            services.append(prod)

        # 6. Criar Orçamentos (Estimates)
        estimates_titles = [
            'Projeto Cozinha e Área de Serviço',
            'Lavatório Suíte Master Carrara',
            'Escada Social Nero Marquina',
            'Varanda Gourmet Completa',
        ]

        for i, title in enumerate(estimates_titles):
            cust = customers[i % len(customers)]
            est, created = Estimate.objects.get_or_create(
                organization=org,
                title=title,
                customer=cust,
                defaults={
                    'status': random.choice(['pricing', 'sent', 'approved']),
                    'service_location': 'Av. Paulista, 1000 - São Paulo/SP',
                    'visit_scheduled_at': timezone.now() + timezone.timedelta(days=random.randint(1, 10)),
                    'scope_summary': f'Fornecimento e instalação de pedras para {title}.',
                    'labor_amount': Decimal('500.00'),
                    'validity_days': 10,
                    'created_by': admin_user
                }
            )
            est.ensure_number()
            if created:
                # Add materials
                for mat in random.sample(materials, 2):
                    EstimateLine.objects.create(
                        estimate=est,
                        product=mat,
                        kind='product',
                        description=f'Fornecimento de {mat.name}',
                        unit='m²',
                        quantity=Decimal(random.randint(2, 8)),
                        unit_price=mat.sale_price
                    )
                # Add services
                for srv in random.sample(services, 2):
                    EstimateLine.objects.create(
                        estimate=est,
                        product=srv,
                        kind='service',
                        description=srv.name,
                        unit='un',
                        quantity=Decimal(1),
                        unit_price=srv.sale_price
                    )
                # Add measurements
                EstimateMeasurement.objects.create(
                    estimate=est,
                    label='Comprimento da bancada principal',
                    value=Decimal('2.45'),
                    unit='m'
                )

        # 7. Criar Relatórios de Vistoria (Service Reports)
        reports_titles = [
            'Medição Técnica Cozinha Carlos',
            'Vistoria de Entrega Lavatório Ana',
        ]

        for i, title in enumerate(reports_titles):
            cust = customers[i % len(customers)]
            est = Estimate.objects.filter(customer=cust).first()
            rep, created = ServiceReport.objects.get_or_create(
                organization=org,
                customer=cust,
                title=title,
                defaults={
                    'estimate': est,
                    'status': 'completed',
                    'technician_name': 'Fabrizio Santander',
                    'problem_reported': 'Fazer medições finais das bancadas para corte.',
                    'service_performed': 'Medição de nível, prumo e alinhamento concluída com sucesso.',
                    'recommendations': 'Garantir que a cuba esteja no local no dia da instalação.',
                    'created_by': admin_user,
                }
            )
            rep.ensure_number()
            if created:
                # Adicionar itens ao relatório
                ServiceReportItem.objects.create(
                    report=rep,
                    description='Medição técnica presencial',
                    quantity=Decimal('1.000'),
                    unit='un',
                    unit_price=Decimal('150.00'),
                    is_billable=True
                )

        self.stdout.write(self.style.SUCCESS('Seed demonstrativo da marmoraria criado com sucesso!'))
