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

        self.user_test_01 = User.objects.create_user(
            username = "first user",
            password = "Password111"
        )
        self.user_test_01.save()

        user_test_02 = User.objects.create_user(
            username = "second user",
            password = "Password222"
        )
        user_test_02.save()

        self.show_test = LaterWatchShow.objects.create(
            user_link = self.user_test_01,
            myshows_id = 12,
            title_eng = "My Show for tests",
            year = 2021
        )
        LaterWatchShow.objects.create(
            user_link = self.user_test_01,
            myshows_id = 24,
            title_eng = "My Show for tests 2",
            year = 2020
        )
        LaterWatchShow.objects.create(
            user_link = user_test_02,
            myshows_id = 36,
            title_eng = "My Show for tests 3",
            year = 1999
        )

        self.show_excepted_data = LaterWatchDetailSerializer(self.show_test).data
        show_queryset = LaterWatchShow.objects.filter(
            user_link = self.user_test_01  
        )
        self.show_excepted_data_list = LaterWatchDetailSerializer(
            show_queryset, many=True).data

        self.data = {
            "user_link": 12,
            "myshows_id": 1112,
            "title_eng": "Test Title",
            "year": 2002
            }
        
        self.long_data = {
            "user_link": 13,
            "myshows_id": 1113,
            "title_eng": "Long long long long long long long long long long long long long long long long long long long long title",
            "year": 2003
            }
        
        self.access_token = self.api_authentication()


    def api_authentication(self):
        """JWT Authentication for test user based by djoser library."""
        jwt_url = reverse('jwt-create')
        jwt_response = self.client.post(
            jwt_url, {'username':'first user', 'password':'Password111'}, format='json'
        )
        access_token = jwt_response.data['access']
        return access_token


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
        record_count = LaterWatchShow.objects.filter(user_link = self.user_test_01).count()
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


    def test_update_action(self):
        """ Test UPDATE request from an authorized user."""
        record_count = LaterWatchShow.objects.count()
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + self.access_token)
        url = reverse('later-watch-shows-detail', kwargs={"pk": self.show_test.id})
        response = self.client.put(url, self.data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response['content-type'], 'application/json')
        self.assertEqual(LaterWatchShow.objects.count(), record_count)
        self.assertEqual(
            json.loads(response.content.decode('utf8'))['title_eng'],
            self.data['title_eng']
        )


    def test_destroy_action(self):
        """ Test DELETE request from an authorized user."""
        record_count = LaterWatchShow.objects.count()
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + self.access_token)
        url = reverse('later-watch-shows-detail', kwargs={"pk": self.show_test.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        #self.assertEqual(response['content-type'], 'application/json')
        self.assertEqual(LaterWatchShow.objects.count(), record_count - 1)


    def test_create_action_with_long_title(self):
        """ Test POST request with field length more than max_length."""
        record_count = LaterWatchShow.objects.count()
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + self.access_token)
        max_length = LaterWatchShow._meta.get_field('title_eng').max_length
        url = reverse('later-watch-shows-list')
        response = self.client.post(url, self.long_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response['content-type'], 'application/json')
        self.assertEqual(
            response.data['title_eng'][0], 
            f'Ensure this field has no more than {max_length} characters.'
        )
        self.assertEqual(LaterWatchShow.objects.count(), record_count)


    def test_not_found_url(self):
        """ Test response for not founded URL."""
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + self.access_token)
        url = reverse('later-watch-shows-detail', kwargs={"pk": randint(100, 900)})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response['content-type'], 'application/json')
