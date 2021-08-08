"""MyShows application URL Configuration"""

from django.urls import path, re_path, include
from rest_framework.routers import DefaultRouter
from .views.later_watch_shows import LaterWatchShowViewSet
from .views.full_watched_shows import FullWatchedShowViewSet
from .views.client_views import *


router = DefaultRouter()
router.register(r'later-watch-shows', LaterWatchShowViewSet, basename='later-watch-shows')
router.register(r'full-watched-shows', FullWatchedShowViewSet, basename='full-watched-shows')

urlpatterns = [
    re_path(r'^api/', include(router.urls)),
    re_path(r'^api/api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    re_path(r'^api/auth/', include('djoser.urls')),
    re_path(r'^api/auth/', include('djoser.urls.jwt')),
    path('', index , name='index'),
    path('search/', search, name='search_list'),
    path('<int:myshows_id>/', detail, name='detail'),
    path('register/', register, name="register"),
    path('start/', start, name='start_page'),
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
]
