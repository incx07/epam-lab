"""Creating tests for RESTful API LaterWatchShow model."""

import json
from random import randint
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient, APITestCase
from myshowsapp.models import FullWatchedShow
from myshowsapp.rest.serializers import FullWatchedDetailSerializer


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

        self.show_test = FullWatchedShow.objects.create(
            user_link = self.user_test_01,
            myshows_id = 12,
            title_eng = "My Show for tests",
            year = 2021,
            rating = 5
        )
        FullWatchedShow.objects.create(
            user_link = self.user_test_01,
            myshows_id = 24,
            title_eng = "My Show for tests 2",
            year = 2020,
            rating = 4
        )
        FullWatchedShow.objects.create(
            user_link = user_test_02,
            myshows_id = 36,
            title_eng = "My Show for tests 3",
            year = 1999,
            rating = 1
        )

        self.show_excepted_data = FullWatchedDetailSerializer(self.show_test).data
        show_queryset = FullWatchedShow.objects.filter(
            user_link = self.user_test_01  
        )
        self.show_excepted_data_list = FullWatchedDetailSerializer(
            show_queryset, many=True).data

        self.data = {
            "user_link": 12,
            "myshows_id": 1112,
            "title_eng": "Test Title",
            "year": 2002,
            "rating": 4
            }
        
        self.invalid_data = {
            "user_link": 13,
            "myshows_id": 1113,
            "title_eng": "Test Title 6",
            "year": 2003,
            "rating": 6
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


    def test_create_action_with_invalid_rating(self):
        """ Test POST request with field 'rating' has invalid choice."""
        record_count = FullWatchedShow.objects.count()
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + self.access_token)
        url = reverse('full-watched-shows-list')
        response = self.client.post(url, self.invalid_data, format="json")
        invalid_rating = self.invalid_data['rating']
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response['content-type'], 'application/json')
        self.assertEqual(
            response.data['rating'][0], 
            f'"{invalid_rating}" is not a valid choice.'
        )
        self.assertEqual(FullWatchedShow.objects.count(), record_count)
