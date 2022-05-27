"""MyShows application URL Configuration"""

from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter
from .views.later_watch_shows import LaterWatchShowViewSet
from .views.full_watched_shows import FullWatchedShowViewSet


router = DefaultRouter()
router.register(r'later-watch-shows', LaterWatchShowViewSet, basename='later-watch-shows')
router.register(r'full-watched-shows', FullWatchedShowViewSet, basename='full-watched-shows')

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^auth/', include('djoser.urls')),
    url(r'^auth/', include('djoser.urls.jwt'))
]
