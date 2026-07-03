import os
from datetime import date

from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.db import IntegrityError, transaction
from django.test import TestCase

from .models import Guardian, SchoolUnit, Student, StudentGuardianLink


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

    def test_portalk12_models_can_be_created(self):
        unit, student, guardian = self.create_portalk12_fixture()
        link = StudentGuardianLink.objects.create(
            student=student,
            guardian=guardian,
            relationship=StudentGuardianLink.Relationship.MOTHER,
            is_primary=True,
        )

        self.assertEqual(str(unit), 'Unidade Teste')
        self.assertEqual(str(student), 'Aluno Teste')
        self.assertEqual(str(guardian), 'Responsável Teste')
        self.assertEqual(str(link), 'Aluno Teste - Responsável Teste')

    def test_student_guardian_link_is_unique(self):
        _, student, guardian = self.create_portalk12_fixture()
        StudentGuardianLink.objects.create(
            student=student,
            guardian=guardian,
            relationship=StudentGuardianLink.Relationship.MOTHER,
        )

        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                StudentGuardianLink.objects.create(
                    student=student,
                    guardian=guardian,
                    relationship=StudentGuardianLink.Relationship.FATHER,
                )

    def test_seed_portalk12_demo_command_creates_minimum_dataset(self):
        call_command('seed_portalk12_demo')

        self.assertGreaterEqual(SchoolUnit.objects.count(), 2)
        self.assertGreaterEqual(Student.objects.count(), 8)
        self.assertGreaterEqual(Guardian.objects.count(), 8)
        self.assertGreaterEqual(StudentGuardianLink.objects.count(), 8)

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

    def test_real_backoffice_lists_return_200_when_authenticated(self):
        self.client.login(username='testuser', password='testpassword')
        for route in ['/app/unidades/', '/app/alunos/', '/app/responsaveis/']:
            response = self.client.get(route)
            self.assertEqual(response.status_code, 200, route)

    def test_real_backoffice_lists_show_seeded_names(self):
        call_command('seed_portalk12_demo')
        self.client.login(username='testuser', password='testpassword')

        units_response = self.client.get('/app/unidades/')
        students_response = self.client.get('/app/alunos/')
        guardians_response = self.client.get('/app/responsaveis/')

        self.assertContains(units_response, 'Unidade Centro')
        self.assertContains(students_response, 'Ana Beatriz Lima')
        self.assertContains(guardians_response, 'Carla Lima')

    def test_real_backoffice_lists_show_empty_state(self):
        self.client.login(username='testuser', password='testpassword')

        self.assertContains(self.client.get('/app/unidades/'), 'Nenhuma unidade escolar cadastrada ainda.')
        self.assertContains(self.client.get('/app/alunos/'), 'Nenhum aluno cadastrado ainda.')
        self.assertContains(self.client.get('/app/responsaveis/'), 'Nenhum responsável cadastrado ainda.')

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

    @staticmethod
    def create_portalk12_fixture():
        unit = SchoolUnit.objects.create(
            name='Unidade Teste',
            slug='unidade-teste',
            city='São Paulo',
            state='SP',
        )
        student = Student.objects.create(
            school_unit=unit,
            full_name='Aluno Teste',
            registration_code='TESTE-001',
            birth_date=date(2014, 1, 20),
            grade_name='5º ano',
            classroom='5º A',
        )
        guardian = Guardian.objects.create(
            full_name='Responsável Teste',
            email='responsavel@example.com',
            phone='(11) 99999-0000',
            document='000.000.000-00',
        )
        return unit, student, guardian
