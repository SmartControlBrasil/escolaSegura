from django.test import TestCase
from apps.policy_guard.models import PrivacyConsentLog

class PublicSiteTests(TestCase):
    def test_home_page_status_code(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_about_page_status_code(self):
        response = self.client.get('/sobre/')
        self.assertEqual(response.status_code, 200)

    def test_contact_page_status_code(self):
        response = self.client.get('/contato/')
        self.assertEqual(response.status_code, 200)

    def test_privacy_page_status_code(self):
        response = self.client.get('/privacidade/')
        self.assertEqual(response.status_code, 200)

    def test_terms_page_status_code(self):
        response = self.client.get('/termos/')
        self.assertEqual(response.status_code, 200)

    def test_contact_form_post_records_consent(self):
        initial_count = PrivacyConsentLog.objects.count()
        response = self.client.post('/contato/', {
            'full-name': 'Maria Oliveira',
            'email': 'maria@test.com',
            'phone': '11999998888',
            'message': 'Gostaria de um orçamento de pia',
            'lgpd_consent': 'on'
        })
        self.assertRedirects(response, '/contato/?success=1')
        self.assertEqual(PrivacyConsentLog.objects.count(), initial_count + 1)
        
        consent = PrivacyConsentLog.objects.last()
        self.assertEqual(consent.name, 'Maria Oliveira')
        self.assertEqual(consent.email, 'maria@test.com')
        self.assertEqual(consent.source, 'contato')
