"""Creating tests for Django REST Framework API service."""

import requests_mock
from django.test import SimpleTestCase
from ..service.drf_api_service import list_later_watch_show, list_full_watched_show, DRF_API_URL


@requests_mock.Mocker()
class DRFAPIServiceTest(SimpleTestCase):
    """Test cases for Django REST Framework API service."""

    def test_list_later_watch_show(self, mock):
        return_data = [
            {'id': 5, 'myshows_id': 2354, 'title_eng': 'Misfits', 'year': 2009},
            {'id': 1, 'myshows_id': 3234, 'title_eng': 'Sherlock', 'year': 2010},
            {'id': 4, 'myshows_id': 234, 'title_eng': 'Lost', 'year': 2005}
        ]
        sorted_data = [
            {'id': 4, 'myshows_id': 234, 'title_eng': 'Lost', 'year': 2005},
            {'id': 5, 'myshows_id': 2354, 'title_eng': 'Misfits', 'year': 2009},
            {'id': 1, 'myshows_id': 3234, 'title_eng': 'Sherlock', 'year': 2010}
        ]
        mock.get(f'{DRF_API_URL}later-watch-shows/', json=return_data, status_code=200)
        response = list_later_watch_show()
        self.assertEqual(sorted_data, response)

    def test_list_full_watched_show(self, mock):
        return_data = [
            {'id': 5, 'myshows_id': 2354, 'title_eng': 'Misfits', 'year': 2009, 'rating': '5'},
            {'id': 1, 'myshows_id': 3234, 'title_eng': 'Sherlock', 'year': 2010, 'rating': '2'},
            {'id': 4, 'myshows_id': 234, 'title_eng': 'Lost', 'year': 2005, 'rating': 'No'}
        ]
        sorted_data = [
            {'id': 4, 'myshows_id': 234, 'title_eng': 'Lost', 'year': 2005, 'rating': 'No'},
            {'id': 5, 'myshows_id': 2354, 'title_eng': 'Misfits', 'year': 2009, 'rating': '5'},
            {'id': 1, 'myshows_id': 3234, 'title_eng': 'Sherlock', 'year': 2010, 'rating': '2'}
        ]
        mock.get(f'{DRF_API_URL}full-watched-shows/', json=return_data, status_code=200)
        response = list_full_watched_show()
        self.assertEqual(sorted_data, response)
