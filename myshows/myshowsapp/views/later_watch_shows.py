from rest_framework import generics
from myshowsapp.models import LaterWatchShow
from myshowsapp.rest.serializers import LaterWatchListSerializer
from myshowsapp.rest.serializers import LaterWatchDetailSerializer


class LaterWatchShowList(generics.ListAPIView):
    queryset = LaterWatchShow.objects.all()
    serializer_class = LaterWatchListSerializer


class LaterWatchShowDetail(generics.RetrieveDestroyAPIView):
    queryset = LaterWatchShow.objects.all()
    serializer_class = LaterWatchDetailSerializer


class LaterWatchShowCreate(generics.CreateAPIView):
    serializer_class = LaterWatchDetailSerializer
