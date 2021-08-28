from django.test import SimpleTestCase
from django.urls import reverse
from unittest.mock import patch
from ..views.auth_views import LoginView, LogoutView, RegisterView


class AuthViewsTest(SimpleTestCase):


    def test_get_login_page(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.resolver_match.func.__name__, LoginView.as_view().__name__)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/login.html')


    @patch('myshowsapp.forms.client')
    def test_redirect_and_set_cookie_after_success_login(self, mock_client):
        mock_client.is_authenticated = True
        credential = {'username':'first user', 'password':'Password111'}
        response = self.client.post(reverse('login'), data=credential)
        self.assertTrue(mock_client.login.called)
        self.assertIn('refresh_token=None; HttpOnly;', str(response.cookies))
        self.assertRedirects(response, '/', target_status_code=302)
    

    def test_redirect_and_delete_cookie_after_logout(self):
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.resolver_match.func.__name__, LogoutView.as_view().__name__)
        self.assertIn('refresh_token="";', str(response.cookies))
        self.assertRedirects(response, '/login/')


    def test_get_register_page(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.resolver_match.func.__name__, RegisterView.as_view().__name__)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/register.html')
