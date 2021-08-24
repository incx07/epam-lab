"""Creating tests for MyShows API service."""

import requests_mock
from django.test import SimpleTestCase
from ..service.myshows_api_service import myshows_search, myshows_getbyid, MYSHOWS_API_URL


@requests_mock.Mocker()
class MyShowsAPIServiceTest(SimpleTestCase):
    """Test cases for API MyShows API service without using database."""

    def test_myshows_search(self, mock):
        """Test myshows_search funtion."""
        return_data = {
            'jsonrpc': '2.0',
            'result': [
                {'id': 123, 'titleOriginal': 'Test title'},
                {'id': 60530, 'titleOriginal': 'Test title 2'},
            ],
            'id': 1
        }
        mock.post(MYSHOWS_API_URL, json=return_data, status_code=200)
        response = myshows_search('Test')
        self.assertEqual(response, return_data)

    def test_myshows_getbyid_success(self, mock):
        """Test myshows_getbyid funtion with successful request."""
        return_data = {
            'jsonrpc': '2.0',
            'result': {'id': 123, 'titleOriginal': 'Test title'},
            'id': 1
        }
        mock.post(MYSHOWS_API_URL, json=return_data, status_code=200)
        response = myshows_getbyid(123)
        self.assertEqual(response, return_data)

    def test_myshows_getbyid_error(self, mock):
        """Test myshows_getbyid funtion with non-existent id."""
        return_data = {
            'jsonrpc': '2.0',
            'id': 1,
            'error': {'code': 404, 'data': 'show was not found'},
        }
        mock.post(MYSHOWS_API_URL, json=return_data, status_code=200)
        response = myshows_getbyid(60000000)
        self.assertEqual(response, 'not found')
