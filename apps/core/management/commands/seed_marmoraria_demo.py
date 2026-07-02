import random
from decimal import Decimal
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils import timezone


from apps.core.infrastructure.models import Supplier, Vehicle
from apps.sales.infrastructure.models import Project
from apps.finance.infrastructure.models import AccountPayable, AccountReceivable
from apps.service_reports.infrastructure.models import ProjectDelivery
from apps.core.infrastructure.models import Organization, CompanyProfile
from apps.customers.infrastructure.models import Customer, CustomerAddress, CustomerContact
from apps.catalog.infrastructure.models import ProductCategory, Product
from apps.estimates.infrastructure.models import Estimate, EstimateLine, EstimateMeasurement
from apps.service_reports.infrastructure.models import ServiceReport, ServiceReportItem
from apps.agents.infrastructure.models import AtlasProspect, VirtualAssistantSession, VirtualAssistantMessage

class Command(BaseCommand):
    help = 'Popula a base com dados de demonstração comercial realistas da Marmoraria360.'

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

        profile, created = CompanyProfile.objects.get_or_create(organization=org)
        profile.trade_name = 'Santander Mármores e Granitos'
        profile.legal_name = 'Santander Mármores e Granitos LTDA'
        profile.cnpj = '12.345.678/0001-99'
        profile.phone = '(11) 4142-1413'
        profile.whatsapp = '(11) 99999-8888'
        profile.email = 'comercial@santandermarmoraria.com.br'
        profile.website = 'www.santandermarmoraria.com.br'
        profile.address = 'Av. Exemplo Comercial, 1000 - Centro'
        profile.city = 'São Paulo'
        profile.state = 'SP'
        profile.business_hours = 'Segunda a Sexta: 08:00 às 18:00'
        profile.slogan = 'Qualidade e sofisticação em mármores e granitos'
        profile.footer_text = 'Orçamento gerado por Marmoraria Santander - Todos os direitos reservados.'
        profile.default_terms = 'Pagamento: 50% de sinal e 50% na entrega. Prazo de entrega: 15 dias úteis após medição final.'
        profile.default_estimate_validity = 15
        profile.privacy_policy = 'Esta é a política de privacidade da Marmoraria Santander.'
        profile.terms_of_use = 'Estes são os termos de uso do sistema da Marmoraria Santander.'
        profile.is_active = True
        profile.save()

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

        # 2. Clientes PF (Residenciais) e PJ (Comerciais)
        clients_data = [
            {'name': 'Carlos Roberto Silva', 'type': 'person', 'email': 'carlos.roberto@gmail.com', 'phone': '(11) 98888-7777', 'city': 'São Paulo', 'state': 'SP', 'notes': 'Cliente residencial interessado em mármore Carrara para suíte master.'},
            {'name': 'Ana Paula Souza', 'type': 'person', 'email': 'ana.souza@yahoo.com.br', 'phone': '(11) 97777-6666', 'city': 'Santo André', 'state': 'SP', 'notes': 'Reforma de cozinha com Silestone e granito na lavanderia.'},
            {'name': 'Marcos Vinícius Oliveira', 'type': 'person', 'email': 'marcos.oliveira@outlook.com', 'phone': '(11) 99123-4567', 'city': 'São Caetano do Sul', 'state': 'SP', 'notes': 'Nicho e soleiras para apartamento novo.'},
            {'name': 'Construtora Alfa LTDA', 'type': 'company', 'email': 'contato@construtoraalfa.com.br', 'phone': '(11) 4004-1234', 'city': 'São Bernardo do Campo', 'state': 'SP', 'notes': 'Parceria comercial para fornecimento de soleiras e bancadas em loteamento residencial.'},
            {'name': 'Juliana Medeiros Arquitetura', 'type': 'company', 'email': 'juliana@jm-arquitetura.com', 'phone': '(11) 96666-5555', 'city': 'São Paulo', 'state': 'SP', 'notes': 'Escritório parceiro. Costuma especificar materiais nobres.'},
            {'name': 'Studio Design & Decora', 'type': 'company', 'email': 'contato@studiodesign.art.br', 'phone': '(11) 3855-9000', 'city': 'São Paulo', 'state': 'SP', 'notes': 'Interesse em tampos de lavatórios em porcelanato esculpido.'},
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
                    'notes': cdata['notes']
                }
            )
            customers.append(cust)
            if created:
                CustomerAddress.objects.create(
                    customer=cust,
                    street='Av. Brigadeiro Luís Antônio' if cdata['type'] == 'person' else 'Av. das Nações Unidas',
                    number=str(random.randint(100, 3000)),
                    complement='Apto 152' if cdata['type'] == 'person' else 'Sala 801',
                    district='Jardins' if cdata['type'] == 'person' else 'Pinheiros',
                    city=cdata['city'],
                    state=cdata['state'],
                    zipcode='01317-001'
                )
                CustomerContact.objects.create(
                    customer=cust,
                    name=f"Contato {cdata['name']}",
                    role='Representante' if cdata['type'] == 'company' else 'Principal',
                    email=cdata['email'],
                    phone=cdata['phone'],
                    is_primary=True
                )

        # 3. Categorias de Materiais
        material_categories = ['Mármore', 'Granito', 'Quartzo', 'Silestone', 'Porcelanato']
        categories = {}
        for cat_name in material_categories:
            slug = cat_name.lower().replace('á', 'a').replace('ó', 'o')
            cat, _ = ProductCategory.objects.get_or_create(
                organization=org,
                slug=slug,
                defaults={'name': cat_name, 'description': f'Chapas e blocos de {cat_name}'}
            )
            categories[cat_name] = cat

        # 4. Criar Materiais (Produtos)
        materials_data = [
            ('Mármore', 'Mármore Carrara Gióia', 'MAR-CAR-GIO', 1100.00, 550.00),
            ('Mármore', 'Mármore Nero Marquina Importado', 'MAR-NER-IMP', 1250.00, 650.00),
            ('Mármore', 'Mármore Crema Marfil Classic', 'MAR-CRE-CLA', 850.00, 420.00),
            ('Granito', 'Granito Preto São Gabriel Polido', 'GRA-PSG-POL', 420.00, 190.00),
            ('Granito', 'Granito Cinza Corumbá Escovado', 'GRA-COR-ESC', 280.00, 110.00),
            ('Granito', 'Granito Branco Itaúnas', 'GRA-BIT-ITA', 390.00, 160.00),
            ('Quartzo', 'Quartzo Branco Estelar Prime', 'QUA-EST-PRI', 1350.00, 700.00),
            ('Quartzo', 'Quartzo Cinza Absoluto', 'QUA-CIN-ABS', 1100.00, 520.00),
            ('Silestone', 'Silestone Cinza Expo Original', 'SIL-EXP-ORI', 1600.00, 850.00),
            ('Silestone', 'Silestone Stellar Red', 'SIL-STE-RED', 1800.00, 950.00),
            ('Porcelanato', 'Porcelanato Calacata Gold 120x120', 'POR-CAL-GOL', 350.00, 180.00),
            ('Porcelanato', 'Porcelanato Pulpis Gray Satin', 'POR-PUL-GRA', 290.00, 140.00),
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
                    'description': f'Material {name} com excelente acabamento e tonalidade padronizada.'
                }
            )
            materials.append(prod)

        # 5. Criar Serviços
        services_data = [
            ('Confecção e Instalação de Bancada', 'SER-BAN-CFC', 320.00),
            ('Confecção e Instalação de Cuba Esculpida', 'SER-PIA-ESC', 450.00),
            ('Confecção e Revestimento de Escada', 'SER-ESC-CFC', 380.00),
            ('Instalação e Ajuste de Soleira', 'SER-SOL-INST', 60.00),
            ('Confecção e Fixação de Nicho de Banheiro', 'SER-NIC-BAN', 140.00),
            ('Montagem e Acabamento de Lavatório', 'SER-LAV-MNT', 220.00),
            ('Montagem de Bancada de Varanda Gourmet', 'SER-VGO-MNT', 450.00),
            ('Confecção e Montagem de Ilha de Cozinha', 'SER-ILH-COZ', 550.00),
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
                    'cost_price': Decimal(price * 0.35),
                    'is_active': True,
                    'description': f'Serviço especializado de {name} com profissionais da marmoraria.'
                }
            )
            services.append(prod)

        # 6. Criar Orçamentos com Status Realistas
        estimates_templates = [
            ('Cozinha Integrada e Ilha Central', 'approved'),
            ('Suíte Master Mármore Carrara', 'sent'),
            ('Nicho e Soleiras Apt 12', 'draft'),
            ('Bancadas Varanda Gourmet Construtora', 'rejected'),
        ]

        for i, (title, status) in enumerate(estimates_templates):
            cust = customers[i % len(customers)]
            est, created = Estimate.objects.get_or_create(
                organization=org,
                title=title,
                customer=cust,
                defaults={
                    'status': status,
                    'service_location': 'Av. Brigadeiro Luís Antônio, 2500 - Jardins, São Paulo/SP',
                    'visit_scheduled_at': timezone.now() + timezone.timedelta(days=random.randint(1, 10)),
                    'scope_summary': f'Fornecimento e instalação de revestimentos nobres para o projeto: {title}.',
                    'labor_amount': Decimal('750.00'),
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
                        quantity=Decimal('0.000'), # Will be calculated by save()
                        length=Decimal('2.500'),
                        width=Decimal('0.600'),
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
                # Adicionar medição
                EstimateMeasurement.objects.create(
                    estimate=est,
                    label='Medição de Alinhamento da Parede',
                    value=Decimal('3.200'),
                    unit='m'
                )

        # 7. Criar Vistorias Técnicas (Service Reports)
        reports_data = [
            ('Medição e Vistoria - Banheiro Social Carlos', 'completed'),
            ('Vistoria e Nivelamento - Varanda Gourmet Ana', 'completed'),
        ]

        for i, (title, status) in enumerate(reports_data):
            cust = customers[i % len(customers)]
            est = Estimate.objects.filter(customer=cust).first()
            rep, created = ServiceReport.objects.get_or_create(
                organization=org,
                customer=cust,
                title=title,
                defaults={
                    'estimate': est,
                    'status': status,
                    'technician_name': 'Fabrizio Santander',
                    'problem_reported': 'Fazer medições milimétricas para corte da chapa no tear.',
                    'service_performed': 'Medições tomadas com laser e conferidas na trena. Alinhamento de paredes aprovado.',
                    'recommendations': 'Cuba deve ser entregue na marmoraria antes do corte do tampo.',
                    'created_by': admin_user,
                }
            )
            rep.ensure_number()
            if created:
                ServiceReportItem.objects.create(
                    report=rep,
                    description='Visita técnica e medição a laser',
                    quantity=Decimal('1.000'),
                    unit='un',
                    unit_price=Decimal('200.00'),
                    is_billable=True
                )

        # 8. Criar Prospects para Robô Atlas (em Revisão Humana)
        prospects_data = [
            {'company_name': 'J. Silva Empreendimentos', 'website': 'http://jsilvamarc.com.br', 'contact_name': 'Julio Silva', 'contact_email': 'julio@jsilvamarc.com.br', 'phone': '(11) 98765-4321', 'city': 'São Paulo', 'state': 'SP', 'source': 'Google Search'},
            {'company_name': 'Gomes & Associados Arquitetos', 'website': 'http://gomesarqs.com.br', 'contact_name': 'Fernanda Gomes', 'contact_email': 'fernanda@gomesarqs.com.br', 'phone': '(11) 99888-1234', 'city': 'Barueri', 'state': 'SP', 'source': 'Instagram Specifier'},
            {'company_name': 'G2 Construtora', 'website': 'http://g2construtora.com.br', 'contact_name': 'Roberto Santos', 'contact_email': 'roberto@g2construtora.com.br', 'phone': '(11) 3211-9000', 'city': 'São Caetano do Sul', 'state': 'SP', 'source': 'LinkedIn Specifier'}
        ]

        for pdata in prospects_data:
            AtlasProspect.objects.get_or_create(
                company_name=pdata['company_name'],
                defaults={
                    'website': pdata['website'],
                    'contact_name': pdata['contact_name'],
                    'contact_email': pdata['contact_email'],
                    'phone': pdata['phone'],
                    'city': pdata['city'],
                    'state': pdata['state'],
                    'source': pdata['source'],
                    'score': 85,
                    'status': 'review',
                    'notes': 'Identificado como escritório com alta demanda de mármore importado.'
                }
            )

        # 9. Criar Sessão do Assistente Virtual
        session, created = VirtualAssistantSession.objects.get_or_create(
            visitor_name='Renata Albuquerque',
            defaults={
                'visitor_email': 'renata@albuquerque.design',
                'visitor_phone': '(11) 98877-2233',
                'channel': 'web',
                'summary': 'Interesse em tampos de lavabo para apartamento duplex nos Jardins.',
                'status': 'open'
            }
        )

        if created:
            VirtualAssistantMessage.objects.create(
                session=session,
                role='user',
                content='Olá, gostaria de saber se vocês trabalham com quartzo branco esculpido.'
            )
            VirtualAssistantMessage.objects.create(
                session=session,
                role='assistant',
                content='Olá Renata! Sim, trabalhamos com Quartzo Branco Estelar e fazemos cubas esculpidas personalizadas. Qual seria a largura aproximada do lavabo?'
            )
            VirtualAssistantMessage.objects.create(
                session=session,
                role='user',
                content='Tem cerca de 1,20m de largura.'
            )

        
        # 10. Novos Modelos (Veículos, Fornecedores, Obras, Entregas, Financeiro)
        # Fornecedores
        suppliers = []
        for sname in ['Granitos Silva', 'Mármores e Cia', 'Inox Design', 'Distribuidora São Paulo']:
            s, _ = Supplier.objects.get_or_create(
                organization=org,
                name=sname,
                defaults={'category': 'Pedras' if 'Silva' in sname or 'Mármore' in sname else 'Insumos', 'city': 'São Paulo', 'phone': '(11) 3222-1111'}
            )
            suppliers.append(s)

        # Veículos
        vehicles = []
        for vdata in [('ABC-1234', 'Fiorino'), ('XYZ-9876', 'HR'), ('MMM-0000', 'Saveiro')]:
            v, _ = Vehicle.objects.get_or_create(
                organization=org,
                plate=vdata[0],
                defaults={'model': vdata[1], 'brand': 'Volkswagen' if 'Saveiro' in vdata[1] else 'Fiat' if 'Fiorino' in vdata[1] else 'Hyundai', 'usage': 'Entregas' if 'HR' in vdata[1] else 'Vistorias'}
            )
            vehicles.append(v)

        # Obras
        projects = []
        for i, est in enumerate(Estimate.objects.all()[:5]):
            p, _ = Project.objects.get_or_create(
                organization=org,
                title=f'Obra {est.customer.name.split()[0]}',
                defaults={'customer': est.customer, 'estimate': est, 'address': est.service_location, 'status': 'production'}
            )
            projects.append(p)

        # Entregas
        for i, proj in enumerate(projects[:3]):
            ProjectDelivery.objects.get_or_create(
                organization=org,
                customer=proj.customer,
                project=proj,
                defaults={'checklist_completed': True, 'customer_accepted': False, 'notes': 'Entrega agendada.'}
            )

        # Financeiro (Contas a Pagar / Receber)
        for i, sup in enumerate(suppliers[:3]):
            AccountPayable.objects.get_or_create(
                organization=org,
                description=f'Fatura {sup.name}',
                defaults={'amount': Decimal('1500.00'), 'due_date': timezone.now().date(), 'status': 'pending'}
            )
        
        for i, proj in enumerate(projects[:3]):
            AccountReceivable.objects.get_or_create(
                organization=org,
                customer=proj.customer,
                description=f'Sinal Obra {proj.title}',
                defaults={'amount': Decimal('5000.00'), 'due_date': timezone.now().date(), 'status': 'paid'}
            )

        self.stdout.write(self.style.SUCCESS('Comando de seed comercial seed_marmoraria_demo concluído com sucesso!'))
