from unittest.mock import patch
from django.test import SimpleTestCase
from django.urls import reverse
from ..views.auth_views import (
    LoginView, LogoutView, RegisterView, PasswordResetView,
    PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
)


class AuthViewsTest(SimpleTestCase):


    def test_render_login_page(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.resolver_match.func.__name__, LoginView.as_view().__name__)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/login.html')


    @patch('myshowsapp.forms.client')
    def test_redirect_and_set_cookie_after_success_login(self, mock_client):
        mock_client.is_authenticated = True
        credential = {'username': 'test user', 'password': 'Password111'}
        response = self.client.post(reverse('login'), data=credential)
        mock_client.login.assert_called_once_with('test user', 'Password111')
        self.assertIn('refresh_token=None; HttpOnly;', str(response.cookies))
        self.assertRedirects(response, '/', target_status_code=302)


    def test_redirect_and_delete_cookie_after_logout(self):
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.resolver_match.func.__name__, LogoutView.as_view().__name__)
        self.assertIn('refresh_token="";', str(response.cookies))
        self.assertRedirects(response, '/login/')


    def test_render_register_page(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.resolver_match.func.__name__, RegisterView.as_view().__name__)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/register.html')


    @patch('myshowsapp.forms.register')
    def test_render_after_success_registration(self, mock_register):
        mock_register.return_value = {'username': 'test user'}
        credential = {
            'username':'test user',
            'email': 'test@test.com',
            'password':'Pass1111',
            're_password':'Pass1111'
        }
        response = self.client.post(reverse('register'), data=credential)
        mock_register.assert_called_once_with('test user', 'test@test.com', 'Pass1111', 'Pass1111')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/register.html')
        self.assertEqual(response.context['usernamevalue'], 'test user')
   

    def test_render_password_reset_page(self):
        response = self.client.get(reverse('password_reset'))
        self.assertEqual(response.resolver_match.func.__name__, PasswordResetView.as_view().__name__)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/password_reset.html')


    @patch('myshowsapp.views.auth_views.pwd_reset_by_email')
    def test_redirect_after_enter_email(self, mock_pwd_reset_by_email):
        credential = {'email': 'test@test.com'}
        response = self.client.post(reverse('password_reset'), data=credential)
        mock_pwd_reset_by_email.assert_called_once_with('test@test.com')
        self.assertRedirects(response, '/password-reset/done/')


    def test_render_password_reset_done_page(self):
        response = self.client.get(reverse('password_reset_done'))
        self.assertEqual(response.resolver_match.func.__name__, PasswordResetDoneView.as_view().__name__)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/password_reset_done.html')


    def test_render_password_reset_confirm_page(self):
        kwargs = {'uidb64': 'MTU', 'token': 'as5hc6-5603ac7359b3e39aa4d840b08049708e'}
        response = self.client.get(reverse('password_reset_confirm', kwargs=kwargs))
        self.assertEqual(response.resolver_match.func.__name__, PasswordResetConfirmView.as_view().__name__)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/password_reset_confirm.html')


    @patch('myshowsapp.views.auth_views.pwd_reset_confirm')
    def test_redirect_after_success_password_confirm(self, mock_pwd_reset_confirm):
        kwargs = {'uidb64': 'MTU', 'token': 'as5hc6-5603ac7359b3e39aa4d840b08049708e'}
        credential = {'password': 'Pass1111','re_password': 'Pass1111'}
        mock_pwd_reset_confirm.return_value = {'success': 'The password has been changed!'}
        response = self.client.post(reverse('password_reset_confirm', kwargs=kwargs), data=credential)
        mock_pwd_reset_confirm.assert_called_once_with(
            'MTU', 'as5hc6-5603ac7359b3e39aa4d840b08049708e', 'Pass1111', 'Pass1111'
        )
        self.assertRedirects(response, '/password-reset/complete/')


    @patch('myshowsapp.views.auth_views.pwd_reset_confirm')
    def test_redirect_after_invalid_password_confirm(self, mock_pwd_reset_confirm):
        kwargs = {'uidb64': 'MTU', 'token': 'as5hc6-5603ac7359b3e39aa4d840b08049708e'}
        credential = {'password': 'Pass1112','re_password': 'Pass1111'}
        mock_pwd_reset_confirm.return_value = {'errors': 'The two password fields did not match.'}
        response = self.client.post(reverse('password_reset_confirm', kwargs=kwargs), data=credential)
        mock_pwd_reset_confirm.assert_called_once_with(
            'MTU', 'as5hc6-5603ac7359b3e39aa4d840b08049708e', 'Pass1112', 'Pass1111'
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/password_reset_confirm.html')
        self.assertEqual(response.context['errors'], 'The two password fields did not match.')


    def test_render_password_reset_complete_page(self):
        response = self.client.get(reverse('password_reset_complete'))
        self.assertEqual(response.resolver_match.func.__name__, PasswordResetCompleteView.as_view().__name__)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/password_reset_complete.html')
