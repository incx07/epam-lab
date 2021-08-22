"""Creating tests for djoser REST API authentication service."""

from django.test import SimpleTestCase
import requests_mock
from ..service.auth_api_service import JWTAuth


@requests_mock.Mocker()
class AuthAPIServiceTest(SimpleTestCase):
    """Test cases for for REST API authentication service."""

    def test_login_success(self, mock):
        auth_service = JWTAuth()
        return_data = {
            'refresh': 'Qt7rI-CKihpGtXVsP62Y0HdQpvPVPByp7pelfKe1qqw',
            'access': 'G-HjqTb9Nmj6O5nIbPDsz_pZTJ07Gf35FhcDi-iK5q0'
        }
        mock.post(auth_service.url_create, json=return_data, status_code=200)
        auth_service.login('test_user', '123456')
        self.assertTrue(auth_service.is_authenticated)
        self.assertEqual(auth_service.refresh_token, 'Qt7rI-CKihpGtXVsP62Y0HdQpvPVPByp7pelfKe1qqw')
        self.assertEqual(auth_service.access_token, 'G-HjqTb9Nmj6O5nIbPDsz_pZTJ07Gf35FhcDi-iK5q0')

    def test_login_error(self, mock):
        auth_service = JWTAuth()
        return_data = {'detail': 'No active account found with the given credentials'}
        mock.post(auth_service.url_create, json=return_data, status_code=401)
        auth_service.login('test_user', '12345')
        self.assertFalse(auth_service.is_authenticated)
        self.assertEqual(auth_service.error, 'No active account found with the given credentials')
