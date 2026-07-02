import os

from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.test import TestCase


User = get_user_model()


class BackofficeTests(TestCase):
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

    def test_login_page_uses_akademi_static_assets(self):
        response = self.client.get('/app/login/')
        self.assertContains(response, 'admin_shell/portalk12/css/style.css')
        self.assertContains(response, 'admin_shell/portalk12/images/background/pic-2.png')

    def test_dashboard_uses_base_shell_and_portalk12_menu(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get('/app/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'PortalK12 Admin')
        self.assertContains(response, 'Controle de Acesso')
        self.assertContains(response, 'SaaS Master')
        self.assertContains(response, 'Template Demo')
        self.assertContains(response, 'dlabnav')

    def test_dashboard_does_not_duplicate_full_legacy_shell(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get('/app/')
        content = response.content.decode()
        self.assertEqual(content.count('class="dlabnav"'), 1)
        self.assertEqual(content.count('class="nav-header"'), 1)

    def test_dashboard_dark_uses_base_shell_and_dark_theme_script(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get('/app/dashboard/dark/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'School Performance')
        self.assertContains(response, "dlabSettingsOptions.version = 'dark'")
        self.assertEqual(response.content.decode().count('class="dlabnav"'), 1)

    def test_dashboard_finance_uses_base_shell_without_wallet_sidebar(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get('/app/dashboard/finance/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Finance Map')
        self.assertContains(response, 'School Expense')
        self.assertContains(response, 'dashboard/dashboard-2.js')
        content = response.content.decode()
        self.assertEqual(content.count('id="wallet-bar"'), 0)
        self.assertEqual(content.count('class="dlabnav"'), 1)
        self.assertContains(response, 'footer out-footer style-2')

    def test_pagamentos_route_still_renders_finance_template(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get('/app/pagamentos/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Finance Map')

    def test_alunos_list_uses_base_shell_and_student_table(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get('/app/alunos/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'New Student Deatils')
        self.assertContains(response, '+ New Student')
        content = response.content.decode()
        self.assertEqual(content.count('class="dlabnav"'), 1)
        self.assertEqual(content.count('id="wallet-bar"'), 0)
        self.assertContains(response, 'footer out-footer style-2')

    def test_alunos_detalhe_renders_student_detail_content(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get('/app/alunos/detalhe/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'View More')
        self.assertEqual(response.content.decode().count('class="dlabnav"'), 1)

    def test_alunos_novo_renders_add_student_form(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get('/app/alunos/novo/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Student Details')
        self.assertContains(response, 'id="datepicker"')
        self.assertContains(response, 'no-img-avatar.png')
        self.assertNotContains(response, 'dashboard/dashboard-1.js')

    def test_colaboradores_list_uses_base_shell_and_teacher_cards(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get('/app/colaboradores/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '+ New Teacher')
        self.assertContains(response, 'Teacher Details')
        content = response.content.decode()
        self.assertEqual(content.count('class="dlabnav"'), 1)
        self.assertEqual(content.count('id="wallet-bar"'), 0)

    def test_colaboradores_detalhe_renders_teacher_detail_content(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get('/app/colaboradores/detalhe/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'View More')
        self.assertEqual(response.content.decode().count('class="dlabnav"'), 1)

    def test_colaboradores_novo_renders_add_teacher_form(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get('/app/colaboradores/novo/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Personal Details')
        self.assertContains(response, 'Save as Draft')
        self.assertContains(response, 'no-img-avatar.png')

    def test_cantina_cardapio_uses_base_shell_and_food_menu(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get('/app/cantina/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Food Menu')
        self.assertContains(response, 'All Means')
        content = response.content.decode()
        self.assertEqual(content.count('class="dlabnav"'), 1)
        self.assertEqual(content.count('id="wallet-bar"'), 0)
        self.assertNotContains(response, 'dashboard/dashboard-1.js')

    def test_pedidos_lanche_renders_food_details_content(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get('/app/pedidos-lanche/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Beef Steak with Fried Potato')
        self.assertContains(response, 'Ingredients')
        self.assertContains(response, 'Total Order')
        self.assertEqual(response.content.decode().count('class="dlabnav"'), 1)

    def test_comunicados_inbox_uses_base_shell(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get('/app/comunicados/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Compose Email')
        self.assertContains(response, 'content-body mh-auto')
        content = response.content.decode()
        self.assertEqual(content.count('class="dlabnav"'), 1)
        self.assertNotContains(response, 'dashboard/dashboard-1.js')

    def test_comunicados_redigir_renders_compose_form(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get('/app/comunicados/redigir/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, ' Subject:')
        self.assertContains(response, 'Send')

    def test_ocorrencias_renders_post_details_content(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get('/app/ocorrencias/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Mitchell C. Shay')
        self.assertContains(response, 'Post Comment')
        self.assertContains(response, 'lightgallery-all.min.js')
        self.assertEqual(response.content.decode().count('class="dlabnav"'), 1)

    def test_operacional_pages_use_base_shell(self):
        self.client.login(username='testuser', password='testpassword')
        cases = [
            ('/app/controle-acesso/', 'widget-timeline style-3'),
            ('/app/catracas/', 'overlay-box'),
            ('/app/cameras/', 'Drag and drop your event'),
            ('/app/visitantes/', 'dz-folder'),
            ('/app/autorizacoes/', 'id="smartwizard"'),
        ]
        for route, marker in cases:
            response = self.client.get(route)
            self.assertEqual(response.status_code, 200, route)
            self.assertContains(response, marker, msg_prefix=route)
            self.assertEqual(response.content.decode().count('class="dlabnav"'), 1, route)
            self.assertNotContains(response, 'dashboard/dashboard-1.js', msg_prefix=route)

    def test_cameras_includes_calendar_assets(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get('/app/cameras/')
        self.assertContains(response, 'fullcalendar-5.11.0/lib/main.css')
        self.assertContains(response, 'js/calendar.js')

    def test_relatorios_sistema_pages_use_base_shell(self):
        self.client.login(username='testuser', password='testpassword')
        cases = [
            ('/app/relatorios/', 'Basic Bar Chart'),
            ('/app/relatorios/', 'chartjs-init.js'),
            ('/app/configuracoes/', 'Input Style'),
            ('/app/perfil/', 'About Me'),
            ('/app/perfil/', 'id="lightgallery"'),
        ]
        seen_routes = set()
        for route, marker in cases:
            response = self.client.get(route)
            self.assertEqual(response.status_code, 200, route)
            self.assertContains(response, marker, msg_prefix=route)
            content = response.content.decode()
            self.assertEqual(content.count('class="dlabnav"'), 1, route)
            self.assertNotContains(response, 'dashboard/dashboard-1.js', msg_prefix=route)
            seen_routes.add(route)
        self.assertEqual(seen_routes, {'/app/relatorios/', '/app/configuracoes/', '/app/perfil/'})

    def test_ui_kit_pages_use_base_shell(self):
        self.client.login(username='testuser', password='testpassword')
        cases = [
            ('/app/ui/tabelas/', 'Basic Datatable', 'highlight.min.js'),
            ('/app/ui/formularios/', 'Input Style', None),
            ('/app/ui/cards/', 'card-title-1', 'highlight.min.js'),
            ('/app/ui/graficos/', 'Chart Morris', 'morris-init.js'),
        ]
        for route, marker, script in cases:
            response = self.client.get(route)
            self.assertEqual(response.status_code, 200, route)
            self.assertContains(response, marker, msg_prefix=route)
            content = response.content.decode()
            self.assertEqual(content.count('class="dlabnav"'), 1, route)
            self.assertNotContains(response, 'dashboard/dashboard-1.js', msg_prefix=route)
            if script:
                self.assertContains(response, script, msg_prefix=route)

    def test_ui_formularios_shows_formularios_heading(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get('/app/ui/formularios/')
        self.assertContains(response, 'Formulários')

    def test_saas_pages_use_base_shell(self):
        self.client.login(username='testuser', password='testpassword')
        cases = [
            ('/app/saas/', 'Timeline', 'widgets-script-init.js'),
            ('/app/saas/tenants/', 'Billing Address', None),
            ('/app/saas/plans/', 'Product code:', None),
            ('/app/saas/subscriptions/', 'Order', None),
        ]
        for route, marker, script in cases:
            response = self.client.get(route)
            self.assertEqual(response.status_code, 200, route)
            self.assertContains(response, marker, msg_prefix=route)
            content = response.content.decode()
            self.assertEqual(content.count('class="dlabnav"'), 1, route)
            self.assertNotContains(response, 'dashboard/dashboard-1.js', msg_prefix=route)
            if script:
                self.assertContains(response, script, msg_prefix=route)

    def test_saas_dashboard_shows_page_heading(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get('/app/saas/')
        self.assertContains(response, 'SaaS Dashboard')

    def test_error_pages_are_standalone_without_shell(self):
        self.client.login(username='testuser', password='testpassword')
        cases = [
            ('/app/erro/404/', '404', 'The page you were looking for is not found!'),
            ('/app/erro/500/', '500', 'Internal Server Error'),
        ]
        for route, code, message in cases:
            response = self.client.get(route)
            self.assertEqual(response.status_code, 200, route)
            self.assertContains(response, message, msg_prefix=route)
            content = response.content.decode()
            self.assertEqual(content.count('class="dlabnav"'), 0, route)
            self.assertEqual(content.count('class="nav-header"'), 0, route)
            self.assertContains(response, 'admin_shell/portalk12/images/student-bg.jpg', msg_prefix=route)
            self.assertContains(response, 'href="/app/"', msg_prefix=route)

    def test_responsaveis_uses_base_shell(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get('/app/responsaveis/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Responsáveis')
        self.assertContains(response, 'Nabila Azalea')
        self.assertEqual(response.content.decode().count('class="dlabnav"'), 1)

    def test_escolas_uses_table_template_not_dashboard_dark(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get('/app/escolas/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Escolas')
        self.assertContains(response, 'Basic Datatable')
        self.assertNotContains(response, 'School Performance')

    def test_template_demo_pages_use_single_shell(self):
        self.client.login(username='testuser', password='testpassword')
        routes = [
            '/app/template/ui-alert/',
            '/app/template/chat/',
            '/app/template/empty-page/',
            '/app/template/chart-flot/',
        ]
        for route in routes:
            response = self.client.get(route)
            self.assertEqual(response.status_code, 200, route)
            self.assertEqual(response.content.decode().count('class="dlabnav"'), 1, route)

    def test_login_post_valid_credentials_redirects_to_dashboard(self):
        response = self.client.post('/app/login/', {'username': 'testuser', 'password': 'testpassword'})
        self.assertRedirects(response, '/app/')

    def test_routes_require_authentication_redirects_to_custom_login(self):
        routes = [
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
        for route in routes:
            response = self.client.get(route)
            self.assertRedirects(response, f'/app/login/?next={route}')

    def test_routes_status_200_if_logged_in(self):
        self.client.login(username='testuser', password='testpassword')
        routes = [
            '/app/',
            '/app/dashboard/dark/',
            '/app/dashboard/finance/',
            '/app/alunos/',
            '/app/alunos/detalhe/',
            '/app/alunos/novo/',
            '/app/colaboradores/',
            '/app/colaboradores/detalhe/',
            '/app/colaboradores/novo/',
            '/app/responsaveis/',
            '/app/turmas/',
            '/app/escolas/',
            '/app/colaboradores/',
            '/app/visitantes/',
            '/app/autorizacoes/',
            '/app/controle-acesso/',
            '/app/catracas/',
            '/app/cameras/',
            '/app/ocorrencias/',
            '/app/comunicados/',
            '/app/comunicados/redigir/',
            '/app/cantina/',
            '/app/pedidos-lanche/',
            '/app/pagamentos/',
            '/app/relatorios/',
            '/app/configuracoes/',
            '/app/perfil/',
            '/app/ui/tabelas/',
            '/app/ui/formularios/',
            '/app/ui/cards/',
            '/app/ui/graficos/',
            '/app/erro/404/',
            '/app/erro/500/',
            '/app/saas/',
            '/app/saas/tenants/',
            '/app/saas/plans/',
            '/app/saas/subscriptions/',
        ]
        for route in routes:
            response = self.client.get(route)
            self.assertEqual(response.status_code, 200, f'Route {route} failed with status {response.status_code}')

    def test_legacy_routes_are_isolated_by_redirect(self):
        self.client.login(username='testuser', password='testpassword')
        for route in ['/app/clientes/', '/app/orcamentos/', '/app/obras/', '/app/vistorias/']:
            response = self.client.get(route)
            self.assertRedirects(response, '/app/')


class SaasBackofficeTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='saasadmin', password='testpassword')

    def test_saas_routes_redirect_anonymous_user_to_login(self):
        routes = ['/app/saas/', '/app/saas/tenants/', '/app/saas/plans/', '/app/saas/subscriptions/']
        for route in routes:
            response = self.client.get(route)
            self.assertRedirects(response, f'/app/login/?next={route}')

    def test_saas_routes_load_with_login(self):
        self.client.login(username='saasadmin', password='testpassword')
        for route in ['/app/saas/', '/app/saas/tenants/', '/app/saas/plans/', '/app/saas/subscriptions/']:
            response = self.client.get(route)
            self.assertEqual(response.status_code, 200)

    def test_saas_tenant_detail_reuses_tenants_template(self):
        self.client.login(username='saasadmin', password='testpassword')
        response = self.client.get('/app/saas/tenants/42/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Billing Address')
        self.assertEqual(response.content.decode().count('class="dlabnav"'), 1)
