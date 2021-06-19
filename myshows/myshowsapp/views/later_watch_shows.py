from rest_framework.response import Response
from rest_framework.views import APIView
from myshowsapp.models import LaterWatchShow
from myshowsapp.rest.serializers import LaterWatchShowSerializer


class LaterWatchShowView(APIView):
    def get(self, request):
        later_watch_shows = LaterWatchShow.objects.all()
        serializer = LaterWatchShowSerializer(later_watch_shows, many=True)
        return Response({"later_watch_shows": serializer.data})
