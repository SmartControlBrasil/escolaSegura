from django.test import TestCase
from django.contrib.auth import get_user_model

User = get_user_model()

class BackofficeTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', 
            password='testpassword'
        )
        # We need an organization or simple settings, but database query shouldn't fail 
        # since we query total counts which just return 0 if empty.

    def test_dashboard_redirects_if_not_logged_in(self):
        response = self.client.get('/app/')
        self.assertRedirects(response, '/admin/login/?next=/app/')

    def test_dashboard_status_code_if_logged_in(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get('/app/')
        self.assertEqual(response.status_code, 200)

    def test_clientes_redirects_if_not_logged_in(self):
        response = self.client.get('/app/clientes/')
        self.assertRedirects(response, '/admin/login/?next=/app/clientes/')

    def test_clientes_status_code_if_logged_in(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get('/app/clientes/')
        self.assertEqual(response.status_code, 200)

    def test_catalogo_redirects_if_not_logged_in(self):
        response = self.client.get('/app/catalogo/')
        self.assertRedirects(response, '/admin/login/?next=/app/catalogo/')

    def test_catalogo_status_code_if_logged_in(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get('/app/catalogo/')
        self.assertEqual(response.status_code, 200)

    def test_orcamentos_redirects_if_not_logged_in(self):
        response = self.client.get('/app/orcamentos/')
        self.assertRedirects(response, '/admin/login/?next=/app/orcamentos/')

    def test_orcamentos_status_code_if_logged_in(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get('/app/orcamentos/')
        self.assertEqual(response.status_code, 200)

    def test_vistorias_redirects_if_not_logged_in(self):
        response = self.client.get('/app/vistorias/')
        self.assertRedirects(response, '/admin/login/?next=/app/vistorias/')

    def test_vistorias_status_code_if_logged_in(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get('/app/vistorias/')
        self.assertEqual(response.status_code, 200)

    def test_relatorios_redirects_if_not_logged_in(self):
        response = self.client.get('/app/relatorios/')
        self.assertRedirects(response, '/admin/login/?next=/app/relatorios/')

    def test_relatorios_status_code_if_logged_in(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get('/app/relatorios/')
        self.assertEqual(response.status_code, 200)
