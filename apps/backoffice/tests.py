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
