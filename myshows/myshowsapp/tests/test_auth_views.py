from django.test import SimpleTestCase
from django.urls import reverse
from unittest.mock import patch
from ..views.auth_views import LoginView


class AuthViewsTest(SimpleTestCase):


    def test_get_login_page(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/login.html')
        self.assertEqual(response.resolver_match.func.__name__, LoginView.as_view().__name__)


    @patch('myshowsapp.forms.client')
    def test_redirect_to_index_page_after_success_login(self, mock_client):
        mock_client.is_authenticated = True
        credential = {'username':'first user', 'password':'Password111'}
        response = self.client.post(reverse('login'), data=credential)
        self.assertTrue(mock_client.login.called)
        self.assertRedirects(response, '/', target_status_code=302)
    
