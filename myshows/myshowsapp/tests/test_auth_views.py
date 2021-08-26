from django.test import SimpleTestCase
from django.urls import reverse
from ..views.auth_views import LoginView
from ..service.auth_api_service import JWTAuth


class AuthViewsTest(SimpleTestCase):

    def setUp(self):
        self.auth_service = JWTAuth()

    def test_login_view(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/login.html')
        self.assertEqual(response.resolver_match.func.__name__, LoginView.as_view().__name__)
