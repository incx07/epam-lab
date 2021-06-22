"""MyShows application URL Configuration"""

from django.urls import path
from .views.later_watch_shows import LaterWatchShowList, LaterWatchShowDetail, LaterWatchShowCreate
from .views.full_watched_show import FullWatchedShowList, FullWatchedShowDetail, FullWatchedShowCreate


urlpatterns = [
    path('later-watch-shows/', LaterWatchShowList.as_view()),
    path('later-watch-shows/<int:pk>/', LaterWatchShowDetail.as_view()),
    path('later-watch-shows/create/', LaterWatchShowCreate.as_view()),
    path('full-watched-shows/', FullWatchedShowList.as_view()),
    path('full-watched-shows/<int:pk>/', FullWatchedShowDetail.as_view()),
    path('full-watched-shows/create/', FullWatchedShowCreate.as_view()),
]
