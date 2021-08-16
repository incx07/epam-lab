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
    path('', IndexView.as_view() , name='index'),
    path('search/', SearchView.as_view(), name='search_list'),
    path('<int:myshows_id>/', DetailView.as_view(), name='detail'),
    path('start/', StartView.as_view(), name='start_page'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('password-reset/', PasswordResetView.as_view(), name='password_reset'),
    path('password-reset/done/', PasswordResetDoneView.as_view(), name='password_reset_done'),
    re_path(r'^password-reset/confirm/(?P<uidb64>[-\w]+)/(?P<token>[-\w]+)/$', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password-reset/complete/', PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]
