"""Creating tests for RESTful API LaterWatchShow model."""

import json
from random import randint
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient, APITestCase
from myshowsapp.models import LaterWatchShow
from myshowsapp.rest.serializers import LaterWatchDetailSerializer


class LaterWatchShowTests(APITestCase):
    """Creating test cases for API LaterWatchShow model."""

    def setUp(self):
        self.client = APIClient()
        user_test = User.objects.create_user(
            username = "john",
            password = "johnpassword"
        )
        user_test.save()
        jwt_url = reverse('jwt-create')
        jwt_response = self.client.post(
            jwt_url, {'username':'john', 'password':'johnpassword'}, format='json'
        )
        self.access_token = jwt_response.data['access']
        self.show_test = LaterWatchShow.objects.create(
            user_link = user_test,
            myshows_id = 12,
            title_eng = "My Show for tests",
            year = 2021
        )
        LaterWatchShow.objects.create(
            user_link = user_test,
            myshows_id = 24,
            title_eng = "My Show for tests 2",
            year = 2020
        )
        self.show_excepted_data = LaterWatchDetailSerializer(self.show_test).data
        show_queryset = LaterWatchShow.objects.all()
        self.show_excepted_data_list = LaterWatchDetailSerializer(
            show_queryset, many=True).data
        self.data = {
            "user_link": 12,
            "myshows_id": 1112,
            "title_eng": "Test Title",
            "year": 2002
            }


    def test_list_action_unauthorized(self):
        """ Test GET request from an unauthorized user."""
        url = reverse('later-watch-shows-list')
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response['content-type'], 'application/json')


    def test_create_action_unauthorized(self):
        """ Test POST request from an unauthorized user."""
        url = reverse('later-watch-shows-list')
        response = self.client.post(url, self.data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response['content-type'], 'application/json')


    def test_update_action_unauthorized(self):
        """ Test UPDATE request from an unauthorized user."""
        url = reverse('later-watch-shows-detail', kwargs={"pk": self.show_test.id})
        response = self.client.put(url, self.data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response['content-type'], 'application/json')


    def test_destroy_action_unauthorized(self):
        """ Test DELETE request from an unauthorized user."""
        url = reverse('later-watch-shows-detail', kwargs={"pk": self.show_test.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response['content-type'], 'application/json')


    def test_list_action(self):
        """ Test GET request (action: list) from an authorized user."""
        record_count = LaterWatchShow.objects.count()
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + self.access_token)
        url = reverse('later-watch-shows-list')
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response['content-type'], 'application/json')
        self.assertEqual(len(response.data), record_count)
        self.assertEqual(
            json.loads(response.content.decode('utf8')),
            self.show_excepted_data_list
            )


    def test_retrieve_action(self):
        """ Test GET request (action: retrieve) from an authorized user."""
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + self.access_token)
        url = reverse('later-watch-shows-detail', kwargs={"pk": self.show_test.id})
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response['content-type'], 'application/json')
        #self.assertEqual(response.json().get("title_eng"), self.show_test.title_eng)
        self.assertEqual(
            json.loads(response.content.decode('utf8')),
            self.show_excepted_data
            )


    def test_create_action(self):
        """ Test POST request from an authorized user."""
        record_count = LaterWatchShow.objects.count()
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + self.access_token)
        url = reverse('later-watch-shows-list')
        response = self.client.post(url, self.data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response['content-type'], 'application/json')
        self.assertEqual(LaterWatchShow.objects.count(), record_count + 1)


    def test_not_found_url(self):
        """ Test response for not founded URL."""
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + self.access_token)
        url = reverse('later-watch-shows-detail', kwargs={"pk": randint(100, 900)})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response['content-type'], 'application/json')
