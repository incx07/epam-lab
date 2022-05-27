"""Creating tests for Django application client views."""

from unittest.mock import patch
from django.test import SimpleTestCase
from django.urls import reverse
from ..views.client_views import SearchView, StartView, DetailView, IndexView


@patch('myshowsapp.views.client_views.client')
class ClientViewsTest(SimpleTestCase):

    def setUp(self):
        self.myshows_getbyid_return_value = {
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

    @patch('myshowsapp.views.client_views.myshows_search')
    def test_render_search_page(self, mock_myshows_search, mock_client):
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
        response = self.client.get(reverse('search_list'), {'search': 'Westworld'})
        self.assertEqual(response.resolver_match.func.__name__, SearchView.as_view().__name__)
        mock_myshows_search.assert_called_once_with('Westworld')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'myshowsapp/search.html')
        self.assertEqual(response.context['searching_results'], expected_data)

    def test_render_start_page_for_unauthorized_user(self, mock_client):
        mock_client.is_authenticated = False
        response = self.client.get(reverse('start_page'))
        self.assertEqual(response.resolver_match.func.__name__, StartView.as_view().__name__)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'myshowsapp/start.html')

    def test_render_start_page_for_authorized_user(self, mock_client):
        mock_client.is_authenticated = True
        response = self.client.get(reverse('start_page'))
        self.assertEqual(response.resolver_match.func.__name__, StartView.as_view().__name__)
        self.assertRedirects(response, '/', fetch_redirect_response=False)

    @patch('myshowsapp.views.client_views.myshows_getbyid')
    def test_render_detail_page_for_unauthorized_user(self, mock_myshows_getbyid, mock_client):
        mock_myshows_getbyid.return_value = self.myshows_getbyid_return_value
        mock_client.is_authenticated = False
        expected_data = mock_myshows_getbyid.return_value['result']
        response = self.client.get(reverse('detail', kwargs={'myshows_id': 123}))
        self.assertEqual(response.resolver_match.func.__name__, DetailView.as_view().__name__)
        mock_myshows_getbyid.assert_called_once_with(123)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'myshowsapp/detail.html')
        self.assertEqual(response.context['result'], expected_data)

    @patch('myshowsapp.views.client_views.list_full_watched_show')
    @patch('myshowsapp.views.client_views.list_later_watch_show')
    @patch('myshowsapp.views.client_views.myshows_getbyid')
    def test_render_detail_page_for_authorized_user_with_unwatched_show(
                    self, mock_myshows_getbyid, mock_list_later_watch_show,
                    mock_list_full_watched_show, mock_client):
        mock_myshows_getbyid.return_value = self.myshows_getbyid_return_value
        mock_client.is_authenticated = True
        mock_list_later_watch_show.return_value = [
            {'id': 4, 'myshows_id': 7718, 'title_eng': 'First show', 'year': 2010}
        ]
        mock_list_full_watched_show.return_value = [
            {'id': 7, 'myshows_id': 8, 'title_eng': 'Second show', 'year': 2019, 'rating': 5}
        ]
        expected_data = mock_myshows_getbyid.return_value['result']
        response = self.client.get(reverse('detail', kwargs={'myshows_id': 123}))
        mock_myshows_getbyid.assert_called_once_with(123)
        mock_list_later_watch_show.assert_called_once_with()
        mock_list_full_watched_show.assert_called_once_with()
        self.assertEqual(response.context['result'], expected_data)
        self.assertTrue(response.context['show_button_later'])
        self.assertTrue(response.context['show_button_full'])

    @patch('myshowsapp.views.client_views.myshows_getbyid')
    def test_render_detail_page_with_invalid_id(
                                    self, mock_myshows_getbyid, mock_client):
        mock_myshows_getbyid.return_value = {'error': 'Show was not found'}
        mock_client.is_authenticated = True
        expected_data = 'Show was not found'
        response = self.client.get(reverse('detail', kwargs={'myshows_id': 12300000000}))
        mock_myshows_getbyid.assert_called_once_with(12300000000)
        self.assertEqual(response.context['not_found'], expected_data)

    @patch('myshowsapp.views.client_views.list_full_watched_show')
    @patch('myshowsapp.views.client_views.list_later_watch_show')
    @patch('myshowsapp.views.client_views.myshows_getbyid')
    def test_render_detail_page_for_authorized_user_with_show_going_to_watch(
                    self, mock_myshows_getbyid, mock_list_later_watch_show,
                    mock_list_full_watched_show, mock_client):
        mock_myshows_getbyid.return_value = self.myshows_getbyid_return_value
        mock_client.is_authenticated = True
        mock_list_later_watch_show.return_value = [
            {'id': 4, 'myshows_id': 123, 'title_eng': 'First show', 'year': 2010}
        ]
        mock_list_full_watched_show.return_value = [
            {'id': 7, 'myshows_id': 124, 'title_eng': 'Second show', 'year': 2021, 'rating': 5}
        ]
        expected_data = mock_myshows_getbyid.return_value['result']
        response = self.client.get(reverse('detail', kwargs={'myshows_id': 123}))
        mock_myshows_getbyid.assert_called_once_with(123)
        mock_list_later_watch_show.assert_called_once_with()
        mock_list_full_watched_show.assert_called_once_with()
        self.assertEqual(response.context['result'], expected_data)
        self.assertFalse(response.context['show_button_later'])
        self.assertTrue(response.context['show_button_full'])

    @patch('myshowsapp.views.client_views.list_full_watched_show')
    @patch('myshowsapp.views.client_views.list_later_watch_show')
    @patch('myshowsapp.views.client_views.myshows_getbyid')
    def test_render_detail_page_for_authorized_user_with_full_watched_show(
                    self, mock_myshows_getbyid, mock_list_later_watch_show,
                    mock_list_full_watched_show, mock_client):
        mock_myshows_getbyid.return_value = self.myshows_getbyid_return_value
        mock_client.is_authenticated = True
        mock_list_later_watch_show.return_value = [
            {'id': 4, 'myshows_id': 7718, 'title_eng': 'First show', 'year': 2010}
        ]
        mock_list_full_watched_show.return_value = [
            {'id': 7, 'myshows_id': 123, 'title_eng': 'Second show', 'year': 2021, 'rating': 5}
        ]
        expected_data = mock_myshows_getbyid.return_value['result']
        response = self.client.get(reverse('detail', kwargs={'myshows_id': 123}))
        mock_myshows_getbyid.assert_called_once_with(123)
        mock_list_later_watch_show.assert_called_once_with()
        mock_list_full_watched_show.assert_called_once_with()
        self.assertEqual(response.context['result'], expected_data)
        self.assertTrue(response.context['show_button_later'])
        self.assertFalse(response.context['show_button_full'])

    @patch('myshowsapp.views.client_views.create_show_later')
    def test_render_detail_page_after_clicking_going_to_watch_button(
                                    self, mock_create_show_later, mock_client):
        url = reverse('detail', kwargs={'myshows_id': 123})
        response = self.client.post(url, data={'add_later': '123'})
        mock_create_show_later.assert_called_once_with(123)
        self.assertRedirects(response, url, fetch_redirect_response=False)
        self.assertEqual(response.resolver_match.func.__name__, DetailView.as_view().__name__)

    @patch('myshowsapp.views.client_views.delete_show_later')
    @patch('myshowsapp.views.client_views.list_later_watch_show')
    @patch('myshowsapp.views.client_views.create_show_full')
    def test_render_detail_page_after_clicking_watcher_all_button(
                    self, mock_create_show_full, mock_list_later_watch_show,
                    mock_delete_show_later, mock_client):
        mock_list_later_watch_show.return_value = [
            {'id': 4, 'myshows_id': 123, 'title_eng': 'First show', 'year': 2010}
        ]
        url = reverse('detail', kwargs={'myshows_id': 123})
        response = self.client.post(url, data={'add_full': '123'})
        mock_create_show_full.assert_called_once_with(123)
        mock_list_later_watch_show.assert_called_once_with()
        mock_delete_show_later.assert_called_once_with(4)
        self.assertRedirects(response, url, fetch_redirect_response=False)
        self.assertEqual(response.resolver_match.func.__name__, DetailView.as_view().__name__)

    def test_render_index_page_for_unauthorized_user(self, mock_client):
        mock_client.is_authenticated = False
        response = self.client.get(reverse('index'))
        self.assertEqual(response.resolver_match.func.__name__, IndexView.as_view().__name__)
        self.assertRedirects(response, '/start/')

    @patch('myshowsapp.views.client_views.list_full_watched_show')
    @patch('myshowsapp.views.client_views.list_later_watch_show')
    def test_render_index_page_for_authorized_user(
                        self, mock_list_later_watch_show,
                        mock_list_full_watched_show, mock_client):
        mock_client.is_authenticated = True
        mock_list_later_watch_show.return_value = [
            {'id': 4, 'myshows_id': 7718, 'title_eng': 'First show', 'year': 2010}
        ]
        mock_list_full_watched_show.return_value = [
            {'id': 7, 'myshows_id': 12, 'title_eng': 'Second show', 'year': 2021, 'rating': 5}
        ]
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'myshowsapp/index.html')
        self.assertEqual(response.resolver_match.func.__name__, IndexView.as_view().__name__)
        self.assertEqual(
            response.context['list_going_to_watch'].object_list,
            mock_list_later_watch_show.return_value
        )
        self.assertEqual(
            response.context['list_watched_all'].object_list,
            mock_list_full_watched_show.return_value
        )

    @patch('myshowsapp.views.client_views.list_full_watched_show')
    @patch('myshowsapp.views.client_views.list_later_watch_show')
    def test_render_index_page_for_authorized_user_with_pagination(
                        self, mock_list_later_watch_show,
                        mock_list_full_watched_show, mock_client):
        mock_client.is_authenticated = True
        mock_list_later_watch_show.return_value = [
            {'id': 1, 'myshows_id': 101, 'title_eng': 'Show 1', 'year': 2010},
            {'id': 2, 'myshows_id': 102, 'title_eng': 'Show 2', 'year': 2011},
            {'id': 3, 'myshows_id': 103, 'title_eng': 'Show 3', 'year': 2012},
            {'id': 4, 'myshows_id': 104, 'title_eng': 'Show 4', 'year': 2013},
            {'id': 5, 'myshows_id': 105, 'title_eng': 'Show 5', 'year': 2014},
            {'id': 6, 'myshows_id': 106, 'title_eng': 'Show 6', 'year': 2015},
        ]
        mock_list_full_watched_show.return_value = [
            {'id': 1, 'myshows_id': 11, 'title_eng': 'Show 7', 'year': 2000, 'rating': 5},
            {'id': 2, 'myshows_id': 12, 'title_eng': 'Show 8', 'year': 2001, 'rating': 5},
            {'id': 3, 'myshows_id': 13, 'title_eng': 'Show 9', 'year': 2002, 'rating': 5},
            {'id': 4, 'myshows_id': 14, 'title_eng': 'Show 1', 'year': 2003, 'rating': 5},
            {'id': 5, 'myshows_id': 15, 'title_eng': 'Show 2', 'year': 2004, 'rating': 5},
            {'id': 6, 'myshows_id': 16, 'title_eng': 'Show 3', 'year': 2005, 'rating': 5},
        ]
        expected_list_later_watch_show = [
            {'id': 6, 'myshows_id': 106, 'title_eng': 'Show 6', 'year': 2015},
        ]
        expected_list_full_watched_show = [
            {'id': 6, 'myshows_id': 16, 'title_eng': 'Show 3', 'year': 2005, 'rating': 5},
        ]
        response = self.client.get(reverse('index'), {'page1': 2, 'page2': 2})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'myshowsapp/index.html')
        self.assertEqual(response.resolver_match.func.__name__, IndexView.as_view().__name__)
        self.assertEqual(
            response.context['list_going_to_watch'].object_list,
            expected_list_later_watch_show
        )
        self.assertEqual(
            response.context['list_watched_all'].object_list,
            expected_list_full_watched_show
        )

    @patch('myshowsapp.views.client_views.list_full_watched_show')
    @patch('myshowsapp.views.client_views.list_later_watch_show')
    @patch('myshowsapp.views.client_views.delete_show_later')
    def test_render_index_page_after_clicking_going_to_watch_delete_button(
                        self, mock_delete_show_later, mock_list_later_watch_show,
                        mock_list_full_watched_show, mock_client):
        response = self.client.post(reverse('index'), data={'del_later': '123'})
        mock_delete_show_later.assert_called_once_with(123)
        mock_list_later_watch_show.assert_called_once_with()
        mock_list_full_watched_show.assert_called_once_with()
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['list_going_to_watch'].object_list)
        self.assertTrue(response.context['list_watched_all'].object_list)

    @patch('myshowsapp.views.client_views.list_full_watched_show')
    @patch('myshowsapp.views.client_views.list_later_watch_show')
    @patch('myshowsapp.views.client_views.delete_show_full')
    def test_render_index_page_after_clicking_watched_all_delete_button(
                        self, mock_delete_show_full, mock_list_later_watch_show,
                        mock_list_full_watched_show, mock_client):
        response = self.client.post(reverse('index'), data={'del_full': '123'})
        mock_delete_show_full.assert_called_once_with(123)
        mock_list_later_watch_show.assert_called_once_with()
        mock_list_full_watched_show.assert_called_once_with()
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['list_going_to_watch'].object_list)
        self.assertTrue(response.context['list_watched_all'].object_list)

    @patch('myshowsapp.views.client_views.list_full_watched_show')
    @patch('myshowsapp.views.client_views.list_later_watch_show')
    def test_render_index_page_after_clicking_change_button(
                        self, mock_list_later_watch_show,
                        mock_list_full_watched_show, mock_client):
        response = self.client.post(reverse('index'), data={'change_rating': '123'})
        mock_list_later_watch_show.assert_called_once_with()
        mock_list_full_watched_show.assert_called_once_with()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['serial_change_id'], 123)
        self.assertTrue(response.context['form_rating'])
        self.assertTrue(response.context['list_going_to_watch'].object_list)
        self.assertTrue(response.context['list_watched_all'].object_list)

    @patch('myshowsapp.views.client_views.list_full_watched_show')
    @patch('myshowsapp.views.client_views.list_later_watch_show')
    @patch('myshowsapp.views.client_views.set_rating')
    def test_render_index_page_after_clicking_save_button(
                        self, mock_set_rating, mock_list_later_watch_show,
                        mock_list_full_watched_show, mock_client):
        response = self.client.post(reverse('index'),
                                    data={'set_rating': '123', 'rating': '4'})
        mock_list_later_watch_show.assert_called_once_with()
        mock_list_full_watched_show.assert_called_once_with()
        mock_set_rating.assert_called_once_with(123, '4')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['list_going_to_watch'].object_list)
        self.assertTrue(response.context['list_watched_all'].object_list)
