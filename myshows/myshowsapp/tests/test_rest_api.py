"""Creating tests for RESTful API LaterWatchShow and FullWatchedShow models."""

from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase
from myshowsapp.models import LaterWatchShow, FullWatchedShow
from myshowsapp.rest.serializers import LaterWatchDetailSerializer, FullWatchedDetailSerializer
from myshowsapp.tests.api_tests_mixin import APITestsMixin

class LaterWatchShowTests(APITestsMixin, APITestCase):
    """Creating test cases for API LaterWatchShow model."""

    model = LaterWatchShow
    serializer = LaterWatchDetailSerializer
    base_url = 'later-watch-shows'


class FullWatchedShowTests(APITestsMixin, APITestCase):
    """Creating test cases for API FullWatchedShow model."""

    model = FullWatchedShow
    serializer = FullWatchedDetailSerializer
    base_url = 'full-watched-shows'
    APITestsMixin.valid_test_data["rating"] = 4
    invalid_rating_test_data = {
        "user_link": 13,
        "myshows_id": 1113,
        "title_eng": "Test Title 6",
        "year": 2003,
        "rating": 6
        }


    def test_create_action_with_invalid_rating(self):
        """ Test POST request when field 'rating' has invalid choice."""
        objects_count = self.model.objects.count()
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + self.access_token)
        url = reverse(f'{self.base_url}-list')
        response = self.client.post(url, self.invalid_rating_test_data, format="json")
        invalid_rating = self.invalid_rating_test_data['rating']
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response['content-type'], 'application/json')
        self.assertEqual(
            response.data['rating'][0],
            f'"{invalid_rating}" is not a valid choice.'
        )
        self.assertEqual(self.model.objects.count(), objects_count)
