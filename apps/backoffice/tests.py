import os
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.management import call_command

User = get_user_model()

class BackofficeTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', 
            password='testpassword'
        )
        # Define environmental variables for command testing
        os.environ['DJANGO_SUPERUSER_USERNAME'] = 'envadmin'
        os.environ['DJANGO_SUPERUSER_EMAIL'] = 'envadmin@test.com'
        os.environ['DJANGO_SUPERUSER_PASSWORD'] = 'EnvAdminPass123!'
        os.environ['DEMO_OWNER_USERNAME'] = 'envdemo'
        os.environ['DEMO_OWNER_EMAIL'] = 'envdemo@test.com'
        os.environ['DEMO_OWNER_PASSWORD'] = 'EnvDemoPass123!'

    def test_bootstrap_demo_users_command(self):
        call_command('bootstrap_demo_users')
        self.assertTrue(User.objects.filter(username='envadmin', is_superuser=True).exists())
        self.assertTrue(User.objects.filter(username='envdemo', is_staff=False).exists())

    def test_seed_marmoraria_demo_command(self):
        call_command('seed_marmoraria_demo')

    def test_routes_require_authentication_redirects_to_custom_login(self):
        routes = [
            '/app/',
            '/app/clientes/',
            '/app/catalogo/',
            '/app/orcamentos/',
            '/app/orcamentos/novo/',
            '/app/vistorias/',
            '/app/relatorios/',
            '/app/redes-sociais/',
            '/app/growth/',
            '/app/atlas/',
            '/app/assistente/',
            '/app/configuracoes/',
            '/app/entregas/',
            '/app/entregas/nova/',
            '/app/obras/',
            '/app/obras/nova/',
            '/app/veiculos/',
            '/app/veiculos/novo/',
            '/app/fornecedores/',
            '/app/fornecedores/novo/',
            '/app/financeiro/',
            '/app/financeiro/novo/',
            '/app/usuarios/',
            '/app/usuarios/novo/',
        ]
        for route in routes:
            response = self.client.get(route)
            self.assertRedirects(response, f'/app/login/?next={route}')

    def test_login_page_returns_200(self):
        response = self.client.get('/app/login/')
        self.assertEqual(response.status_code, 200)

    def test_login_post_valid_credentials_redirects_to_dashboard(self):
        response = self.client.post('/app/login/', {
            'username': 'testuser',
            'password': 'testpassword'
        })
        self.assertRedirects(response, '/app/')

    def test_login_post_invalid_credentials_returns_error(self):
        response = self.client.post('/app/login/', {
            'username': 'testuser',
            'password': 'wrongpassword'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn("Usuário ou senha incorretos.", response.context['errors'])

    def test_inactive_user_cannot_login(self):
        self.user.is_active = False
        self.user.save()
        response = self.client.post('/app/login/', {
            'username': 'testuser',
            'password': 'testpassword'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn("Usuário ou senha incorretos.", response.context['errors'])

    def test_django_admin_login_continues_working(self):
        response = self.client.get('/admin/login/')
        self.assertEqual(response.status_code, 200)

    def test_routes_status_200_if_logged_in(self):
        call_command('seed_marmoraria_demo')
        self.client.login(username='testuser', password='testpassword')
        
        routes = [
            '/app/',
            '/app/clientes/',
            '/app/catalogo/',
            '/app/orcamentos/',
            '/app/orcamentos/novo/',
            '/app/vistorias/',
            '/app/relatorios/',
            '/app/redes-sociais/',
            '/app/growth/',
            '/app/atlas/',
            '/app/assistente/',
            '/app/configuracoes/',
        ]
        for route in routes:
            response = self.client.get(route)
            self.assertEqual(response.status_code, 200, f"Route {route} failed with status {response.status_code}")

    def test_orcamentos_novo_post(self):
        call_command('seed_marmoraria_demo')
        from apps.customers.infrastructure.models import Customer
        customer = Customer.objects.first()
        self.client.login(username='testuser', password='testpassword')
        
        response = self.client.post('/app/orcamentos/novo/', {
            'customer': str(customer.id),
            'title': 'Test Budget Project',
            'service_location': 'Street Test 123',
            'scope_summary': 'This is a test scope description.'
        })
        self.assertRedirects(response, '/app/orcamentos/')
        
    def test_logged_in_user_accessing_login_redirects_to_dashboard(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get('/app/login/')
        self.assertRedirects(response, '/app/')

    def test_estimate_line_calculation(self):
        call_command('seed_marmoraria_demo')
        from apps.estimates.infrastructure.models import Estimate, EstimateLine
        from apps.catalog.infrastructure.models import Product
        from decimal import Decimal
        
        est = Estimate.objects.first()
        prod = Product.objects.first()
        
        # Test calculation with length and width
        line = EstimateLine.objects.create(
            estimate=est,
            product=prod,
            length=Decimal('2.000'),
            width=Decimal('3.000'),
            unit_price=Decimal('100.00'),
            discount_amount=Decimal('50.00')
        )
        
        self.assertEqual(line.quantity, Decimal('6.000')) # 2 * 3
        self.assertEqual(line.subtotal, Decimal('550.00')) # (6 * 100) - 50
        
    def test_orcamento_preview_route(self):
        call_command('seed_marmoraria_demo')
        from apps.estimates.infrastructure.models import Estimate
        est = Estimate.objects.first()
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(f'/app/orcamentos/{est.id}/preview/')
        self.assertEqual(response.status_code, 200)

    def test_orcamento_pdf_route(self):
        call_command('seed_marmoraria_demo')
        from apps.estimates.infrastructure.models import Estimate
        est = Estimate.objects.first()
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(f'/app/orcamentos/{est.id}/pdf/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/pdf')

    def test_entrega_pdf_route(self):
        call_command('seed_marmoraria_demo')
        from apps.service_reports.infrastructure.models import ProjectDelivery
        
        # Create one delivery if it doesn't exist
        deliv = ProjectDelivery.objects.first()
        if not deliv:
            from apps.customers.infrastructure.models import Customer
            from apps.core.infrastructure.models import Organization
            c = Customer.objects.first()
            org = Organization.objects.first()
            deliv = ProjectDelivery.objects.create(customer=c, organization=org)
            
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(f'/app/entregas/{deliv.id}/pdf/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/pdf')

    def test_configuracoes_empresa_requires_login(self):
        response = self.client.get('/app/configuracoes/empresa/')
        self.assertRedirects(response, '/app/login/?next=/app/configuracoes/empresa/')

    def test_configuracoes_empresa_status_200_if_logged_in(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get('/app/configuracoes/empresa/')
        self.assertEqual(response.status_code, 200)

    def test_seed_creates_company_profile(self):
        from apps.core.infrastructure.models import CompanyProfile
        CompanyProfile.objects.all().delete()
        call_command('seed_marmoraria_demo')
        self.assertTrue(CompanyProfile.objects.filter(trade_name='Santander Mármores e Granitos').exists())

    def test_configuracoes_empresa_post_success(self):
        from apps.core.infrastructure.models import CompanyProfile
        call_command('seed_marmoraria_demo')
        self.user.role = 'owner'
        self.user.save()
        self.client.login(username='testuser', password='testpassword')
        
        response = self.client.post('/app/configuracoes/empresa/', {
            'trade_name': 'New Trade Name',
            'legal_name': 'New Legal Name LTDA',
            'cnpj': '99.999.999/9999-99',
            'phone': '1122223333',
            'whatsapp': '11988887777',
            'email': 'new@company.com',
            'website': 'http://newcompany.com',
            'address': 'New Address 123',
            'city': 'New City',
            'state': 'PR',
            'business_hours': '09:00 - 17:00',
            'slogan': 'The best company',
            'footer_text': 'Footer test',
            'default_terms': 'Terms test',
            'default_estimate_validity': '10',
            'is_active': 'on',
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn("Configurações da empresa salvas com sucesso!", response.context['success_message'])
        
        profile = CompanyProfile.objects.first()
        self.assertEqual(profile.trade_name, 'New Trade Name')
        self.assertEqual(profile.cnpj, '99.999.999/9999-99')

    def test_configuracoes_empresa_post_permission_denied(self):
        from apps.core.infrastructure.models import CompanyProfile
        call_command('seed_marmoraria_demo')
        self.user.role = 'viewer'
        self.user.save()
        self.client.login(username='testuser', password='testpassword')
        
        initial_name = CompanyProfile.objects.first().trade_name
        
        response = self.client.post('/app/configuracoes/empresa/', {
            'trade_name': 'Hacker Name',
            'legal_name': 'Hacker Legal Name',
            'default_estimate_validity': '10',
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn("Apenas usuários dos grupos Proprietário ou Admin Técnico podem salvar alterações.", response.context['error_message'])
        
        profile = CompanyProfile.objects.first()
        self.assertEqual(profile.trade_name, initial_name)
