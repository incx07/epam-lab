from rest_framework import viewsets, permissions
from myshowsapp.models import LaterWatchShow
from myshowsapp.rest.serializers import LaterWatchDetailSerializer
from myshowsapp.permissions import IsOwnerOrReadOnly


class LaterWatchShowLViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.

    """
    queryset = LaterWatchShow.objects.all()
    serializer_class = LaterWatchDetailSerializer
    permission_classes = (permissions.IsAuthenticated, IsOwnerOrReadOnly)
