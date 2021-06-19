from django.urls import path
from .views.later_watch_shows import LaterWatchShowView


urlpatterns = [
    path('later-watch-shows/', LaterWatchShowView.as_view()),
]
