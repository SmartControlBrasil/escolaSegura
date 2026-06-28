from django.test import TestCase

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
