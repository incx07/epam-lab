from django.urls import path
from .views.later_watch_shows import LaterWatchShowList, LaterWatchShowDetail


urlpatterns = [
    path('later-watch-shows/', LaterWatchShowList.as_view()),
    path('later-watch-shows/<int:pk>/', LaterWatchShowDetail.as_view()),
]
