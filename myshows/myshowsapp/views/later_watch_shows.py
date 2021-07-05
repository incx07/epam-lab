"""Creating API Endpoins for LaterWatchShow model."""

from rest_framework import viewsets, permissions
from myshowsapp.models import LaterWatchShow
from myshowsapp.rest.serializers import LaterWatchDetailSerializer
from myshowsapp.permissions import IsOwnerOrReadOnly


class LaterWatchShowViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions for LaterWatchShow model.

    """
    queryset = LaterWatchShow.objects.all()
    serializer_class = LaterWatchDetailSerializer
    permission_classes = (permissions.IsAuthenticated, IsOwnerOrReadOnly)

    def perform_create(self, serializer):
        """When a show is saved, its saved how it is the owner."""
        serializer.save(user_link=self.request.user)

    def get_queryset(self):
        """List of shows will be filtered by owner and return the queryset"""
        owner_queryset = self.queryset.filter(user_link=self.request.user)
        return owner_queryset
