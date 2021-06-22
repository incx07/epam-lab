from rest_framework import generics
from myshowsapp.models import FullWatchedShow
from myshowsapp.rest.serializers import FullWatchedListSerializer
from myshowsapp.rest.serializers import FullWatchedDetailSerializer


class FullWatchedShowList(generics.ListAPIView):
    queryset = FullWatchedShow.objects.all()
    serializer_class = FullWatchedListSerializer


class FullWatchedShowDetail(generics.RetrieveDestroyAPIView):
    queryset = FullWatchedShow.objects.all()
    serializer_class = FullWatchedDetailSerializer


class FullWatchedShowCreate(generics.CreateAPIView):
    serializer_class = FullWatchedDetailSerializer
