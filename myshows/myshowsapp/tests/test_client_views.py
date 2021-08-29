from unittest.mock import patch
from django.test import SimpleTestCase
from django.urls import reverse
from ..views.client_views import SearchView, StartView


class ClientViewsTest(SimpleTestCase):


    @patch('myshowsapp.views.client_views.myshows_search')
    def test_render_search_page(self, mock_myshows_search):
        payload = {'search': 'Westworld'}
        mock_myshows_search.return_value = {
            'jsonrpc': '2.0',
            'result': [
                {'id': 45534, 'titleOriginal': 'Westworld'},
                {'id': 32204, 'titleOriginal': 'Beyond Westworld'},
            ],
            'id': 1
        }
        expected_data = [
            {'id': 45534, 'title_eng': 'Westworld'},
            {'id': 32204, 'title_eng': 'Beyond Westworld'},
        ]
        response = self.client.get(reverse('search_list'), params=payload)
        self.assertEqual(response.resolver_match.func.__name__, SearchView.as_view().__name__)
        self.assertTrue(mock_myshows_search.called)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'myshowsapp/search.html')
        self.assertEqual(response.context['searching_results'], expected_data)


    @patch('myshowsapp.views.client_views.client')
    def test_render_start_page_for_unauthorized_user(self, mock_client):
        mock_client.is_authenticated = False
        response = self.client.get(reverse('start_page'))
        self.assertEqual(response.resolver_match.func.__name__, StartView.as_view().__name__)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'myshowsapp/start.html')


    @patch('myshowsapp.views.client_views.client')
    def test_render_start_page_for_authorized_user(self, mock_client):
        mock_client.is_authenticated = True
        response = self.client.get(reverse('start_page'))
        self.assertEqual(response.resolver_match.func.__name__, StartView.as_view().__name__)
        self.assertRedirects(response, '/', fetch_redirect_response=False)

