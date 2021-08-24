"""Creating tests for djoser REST API authentication service."""

import requests_mock
from django.test import SimpleTestCase
from ..service.auth_api_service import JWTAuth, Registration, AUTH_API_URL, password_reset_confirm


@requests_mock.Mocker()
class AuthAPIServiceTest(SimpleTestCase):
    """Test cases for REST API authentication service."""

    def setUp(self):
        self.auth_service = JWTAuth()

    def test_login_success(self, mock):
        return_data = {
            'refresh': 'secret_refresh_token',
            'access': 'secret_access_token'
        }
        mock.post(self.auth_service.url_create, json=return_data, status_code=200)
        self.auth_service.login('test_user', '123456')
        self.assertTrue(self.auth_service.is_authenticated)
        self.assertEqual(self.auth_service.refresh_token, 'secret_refresh_token')
        self.assertEqual(self.auth_service.access_token, 'secret_access_token')

    def test_login_error(self, mock):
        return_data = {'detail': 'No active account found with the given credentials'}
        mock.post(self.auth_service.url_create, json=return_data, status_code=401)
        self.auth_service.login('test_user', '12345')
        self.assertFalse(self.auth_service.is_authenticated)
        self.assertEqual(self.auth_service.error, 'No active account found with the given credentials')

    def test_get_username_success(self, mock):
        return_data = {'username': 'TestUser'}
        self.auth_service.access_token = 'valid_token'
        mock.get(f'{AUTH_API_URL}users/me/', json=return_data, status_code=200)
        response = self.auth_service.get_username()
        self.assertEqual(response, 'TestUser')

    def test_get_username_error(self, mock):
        return_data = {'detail': 'Given token not valid for any token type'}
        self.auth_service.access_token = 'invalid_token'
        mock.get(f'{AUTH_API_URL}users/me/', json=return_data, status_code=401)
        response = self.auth_service.get_username()
        self.assertIsNone(response)

    def test_refresh_success(self, mock):
        return_data = {'access': 'new_secret_token'}
        mock.post(self.auth_service.url_refresh, json=return_data, status_code=200)
        self.auth_service.refresh('valid_refresh_token')
        self.assertTrue(self.auth_service.is_authenticated)
        self.assertEqual(self.auth_service.access_token, 'new_secret_token')

    def test_refresh_error(self, mock):
        return_data = {'detail': 'Token is invalid or expired'}
        mock.post(self.auth_service.url_refresh, json=return_data, status_code=401)
        self.auth_service.refresh('invalid_refresh_token')
        self.assertFalse(self.auth_service.is_authenticated)
        self.assertIsNone(self.auth_service.username)

    def test_registration_success(self, mock):
        registration = Registration()
        return_data = {'username': 'NewUser'}
        mock.post(f'{AUTH_API_URL}users/', json=return_data, status_code=201)
        registration.register('NewUser', 'test@test.com', 'password', 'password')
        self.assertTrue(registration.is_registered)
        self.assertEqual(registration.username, 'NewUser')

    def test_registration_error(self, mock):
        registration = Registration()
        return_data = {'password': 'This password is entirely numeric.'}
        mock.post(f'{AUTH_API_URL}users/', json=return_data, status_code=400)
        registration.register('NewUser', 'test@test.com', '123', '123')
        self.assertFalse(registration.is_registered)
        self.assertEqual(registration.errors, 'This password is entirely numeric.')

    def test_password_reset_confirm_success(self, mock):
        mock.post(f'{AUTH_API_URL}users/reset_password_confirm/', json=None, status_code=204)
        response = password_reset_confirm('uid', 'token', 'password', 'password')
        self.assertFalse(response)

    def test_password_reset_confirm_error(self, mock):
        return_data = {'new_password': 'This password is entirely numeric.'}
        mock.post(f'{AUTH_API_URL}users/reset_password_confirm/', json=return_data, status_code=400)
        response = password_reset_confirm('uid', 'token', '123', '123')
        self.assertEqual(response, 'This password is entirely numeric.')
