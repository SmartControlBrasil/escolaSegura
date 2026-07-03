import os

from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.test import TestCase


User = get_user_model()


class BackofficeSmokeTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        os.environ['DJANGO_SUPERUSER_USERNAME'] = 'envadmin'
        os.environ['DJANGO_SUPERUSER_EMAIL'] = 'envadmin@test.com'
        os.environ['DJANGO_SUPERUSER_PASSWORD'] = 'EnvAdminPass123!'
        os.environ['DEMO_OWNER_USERNAME'] = 'envdemo'
        os.environ['DEMO_OWNER_EMAIL'] = 'envdemo@test.com'
        os.environ['DEMO_OWNER_PASSWORD'] = 'EnvDemoPass123!'

    def test_bootstrap_demo_users_command(self):
        call_command('bootstrap_demo_users')
        self.assertTrue(User.objects.filter(username='envadmin', is_superuser=True).exists())
        self.assertTrue(User.objects.filter(username='envdemo').exists())

    def test_seed_escola_segura_demo_command(self):
        call_command('seed_escola_segura_demo')

    def test_login_page_returns_200(self):
        response = self.client.get('/app/login/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'admin_shell/portalk12/page-login.html')
        self.assertContains(response, 'Entrar')
        self.assertContains(response, 'name="username"')
        self.assertContains(response, 'csrfmiddlewaretoken')

    def test_login_post_valid_credentials_redirects_to_dashboard(self):
        response = self.client.post('/app/login/', {'username': 'testuser', 'password': 'testpassword'})
        self.assertRedirects(response, '/app/')

    def test_backoffice_routes_require_login(self):
        for route in self.required_smoke_routes():
            response = self.client.get(route)
            self.assertRedirects(response, f'/app/login/?next={route}', msg_prefix=route)

    def test_backoffice_module_routes_render_mocked_pages(self):
        self.client.login(username='testuser', password='testpassword')
        expected_titles = {
            '/app/': 'Dashboard',
            '/app/alunos/': 'Alunos',
            '/app/responsaveis/': 'Responsáveis',
            '/app/turmas/': 'Turmas',
            '/app/unidades/': 'Unidades',
            '/app/colaboradores/': 'Colaboradores',
            '/app/visitantes/': 'Visitantes',
            '/app/controle-acesso/': 'Controle de Acesso',
            '/app/catracas/': 'Catracas',
            '/app/cameras/': 'Câmeras',
            '/app/ocorrencias/': 'Ocorrências',
            '/app/comunicados/': 'Comunicados',
            '/app/cantina/': 'Cantina',
            '/app/pedidos-lanche/': 'Pedidos de Lanche',
            '/app/pagamentos/': 'Pagamentos',
            '/app/relatorios/': 'Relatórios',
            '/app/configuracoes/': 'Configurações',
        }
        forbidden_terms = ['Marmoraria', 'marmoraria', 'Obras', 'obras', 'Orçamentos', 'orçamentos']

        for route, title in expected_titles.items():
            response = self.client.get(route)
            self.assertEqual(response.status_code, 200, route)
            self.assertTemplateUsed(response, 'admin_shell/portalk12/mock_page.html')
            self.assertContains(response, title, msg_prefix=route)
            self.assertContains(response, 'PortalK12 Admin', msg_prefix=route)
            self.assertContains(response, 'dlabnav', msg_prefix=route)
            self.assertContains(response, 'breadcrumb', msg_prefix=route)
            self.assertContains(response, '<table', msg_prefix=route)
            for term in forbidden_terms:
                self.assertNotContains(response, term, msg_prefix=route)

    def test_sidebar_reflects_portalk12_modules(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get('/app/')
        menu_labels = [
            'Dashboard', 'Alunos', 'Responsáveis', 'Turmas', 'Unidades', 'Colaboradores',
            'Visitantes', 'Controle de Acesso', 'Catracas', 'Câmeras', 'Ocorrências',
            'Comunicados', 'Cantina', 'Pedidos de Lanche', 'Pagamentos', 'Relatórios',
            'Configurações',
        ]
        for label in menu_labels:
            self.assertContains(response, label)

    def test_legacy_routes_are_isolated_by_redirect(self):
        self.client.login(username='testuser', password='testpassword')
        for route in ['/app/clientes/', '/app/orcamentos/', '/app/obras/', '/app/vistorias/']:
            response = self.client.get(route)
            self.assertRedirects(response, '/app/', msg_prefix=route)

    @staticmethod
    def required_smoke_routes():
        return [
            '/app/',
            '/app/alunos/',
            '/app/responsaveis/',
            '/app/controle-acesso/',
            '/app/catracas/',
            '/app/cameras/',
            '/app/ocorrencias/',
            '/app/cantina/',
            '/app/pedidos-lanche/',
            '/app/relatorios/',
            '/app/configuracoes/',
        ]
