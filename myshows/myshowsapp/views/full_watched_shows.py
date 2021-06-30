from rest_framework import viewsets, permissions
from myshowsapp.models import FullWatchedShow
from myshowsapp.rest.serializers import FullWatchedDetailSerializer
from myshowsapp.permissions import IsOwnerOrReadOnly


class FullWatchedShowLViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.

    """
    queryset = FullWatchedShow.objects.all()
    serializer_class = FullWatchedDetailSerializer
    permission_classes = (permissions.IsAuthenticated, IsOwnerOrReadOnly)
