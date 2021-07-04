"""MyShows application URL Configuration"""

from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter
from .views.later_watch_shows import LaterWatchShowLViewSet
from .views.full_watched_shows import FullWatchedShowLViewSet


router = DefaultRouter()
router.register(r'later-watch-shows', LaterWatchShowLViewSet)
router.register(r'full-watched-shows', FullWatchedShowLViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^auth/', include('djoser.urls')),
    url(r'^auth/', include('djoser.urls.jwt'))
]
