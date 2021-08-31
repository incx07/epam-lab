from unittest.mock import patch
from django.test import SimpleTestCase
from django.urls import reverse
from ..views.client_views import SearchView, StartView, DetailView


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


    @patch('myshowsapp.views.client_views.client')
    @patch('myshowsapp.views.client_views.myshows_getbyid')
    def test_render_detail_page_for_unauthorized_user(self, mock_myshows_getbyid, mock_client):
        mock_myshows_getbyid.return_value = {
            'jsonrpc': '2.0',
            'result': {
                'id': 123,
                'title': 'Заголовок',
                'titleOriginal': 'Title',
                'description': '<p>Длинное описание</p>',
                'status': 'Canceled/Ended',
                'countryTitle': 'Япония',
                'started': 'Apr/07/2003',
                'ended': 'Mar/24/2012',
                'year': 2003,
                'kinopoiskRating': 7.892,
                'imdbRating': 7.8,
                'image': 'https://media.myshows.me/shows/normal/2/c5/21.jpg',
            },
            'id': 1
        }
        mock_client.is_authenticated = False
        expected_data = mock_myshows_getbyid.return_value['result']
        response = self.client.get(reverse('detail', kwargs={'myshows_id': 123}))
        self.assertEqual(response.resolver_match.func.__name__, DetailView.as_view().__name__)
        self.assertTrue(mock_myshows_getbyid.called)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'myshowsapp/detail.html')
        self.assertEqual(response.context['result'], expected_data)
