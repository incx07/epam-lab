from django.test import SimpleTestCase
from django.urls import reverse


class AuthViewsTest(SimpleTestCase):

    def test_login_view(self):
        response = self.client.get(reverse('login'))
        self.assertTemplateUsed(response, 'registration/login.html')
