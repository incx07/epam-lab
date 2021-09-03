"""Creating tests for Django REST Framework API service."""

from unittest.mock import patch
import requests_mock
from django.test import SimpleTestCase
from ..service.drf_api_service import (
    list_later_watch_show, list_full_watched_show, create_show_later,
    create_show_full, delete_show_later, delete_show_full, set_rating, DRF_API_URL
)


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
        self.assertEqual(mock.call_count, 1)
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
        self.assertEqual(mock.call_count, 1)
        self.assertEqual(sorted_data, response)

    @patch('myshowsapp.service.drf_api_service.myshows_getbyid')
    def test_create_show_later(self, mock, mock_myshows_getbyid):
        mock.post(f'{DRF_API_URL}later-watch-shows/', status_code=201)
        create_show_later(myshows_id=123)
        mock_myshows_getbyid.assert_called_once_with(123)
        self.assertEqual(mock.call_count, 1)

    @patch('myshowsapp.service.drf_api_service.myshows_getbyid')
    def test_create_show_full(self, mock, mock_myshows_getbyid):
        mock.post(f'{DRF_API_URL}full-watched-shows/', status_code=201)
        create_show_full(myshows_id=123)
        mock_myshows_getbyid.assert_called_once_with(123)
        self.assertEqual(mock.call_count, 1)

    def test_delete_show_later(self, mock):
        test_id = 123
        mock.delete(f'{DRF_API_URL}later-watch-shows/{test_id}', status_code=204)
        delete_show_later(id=test_id)
        self.assertEqual(mock.call_count, 1)

    def test_delete_show_full(self, mock):
        test_id = 123
        mock.delete(f'{DRF_API_URL}full-watched-shows/{test_id}', status_code=204)
        delete_show_full(id=test_id)
        self.assertEqual(mock.call_count, 1)

    def test_set_rating(self, mock):
        test_id = 123
        mock.patch(f'{DRF_API_URL}full-watched-shows/{test_id}/', status_code=200)
        set_rating(id=test_id, rating=4)
        self.assertEqual(mock.call_count, 1)
