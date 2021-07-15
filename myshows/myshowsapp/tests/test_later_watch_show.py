"""
Module for creating tests.
"""

from django.http import response
from django.test import Client
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from rest_framework.reverse import reverse
from django.contrib.auth.models import User
from myshowsapp.models import LaterWatchShow


class LaterWatchShowTests(APITestCase):

    def setUp(self):
        self.client = APIClient()
        user_test_01 = User.objects.create_user(
            username = "john", 
            password = "johnpassword"
        )
        user_test_01.save()
        jwt_url = reverse('jwt-create')
        jwt_response = self.client.post(jwt_url, {'username':'john', 'password':'johnpassword'}, format='json')
        self.access_token = jwt_response.data['access']
        self.show_test_01 = LaterWatchShow.objects.create(
            user_link = user_test_01,
            myshows_id = 12,
            title_eng = "My Show for tests",
            year = 2021
        )
        self.data = {
            "user_link": 12,
            "myshows_id": 1112,
            "title_eng": "Test Title",
            "year": 2002
            }

    def test_create_invalid_record(self):
        url = reverse('later-watch-shows-list')
        response = self.client.post(url, self.data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


    def test_create_valid_record(self):
        url = reverse('later-watch-shows-list')
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + self.access_token)
        response = self.client.post(url, self.data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
