"""Description of the data serialization methods."""

from rest_framework import serializers
from myshowsapp.models import LaterWatchShow, FullWatchedShow


class LaterWatchDetailSerializer(serializers.ModelSerializer):
    """Serializer for LaterWatchShow model (return detail information)"""
    user_link = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = LaterWatchShow
        fields = '__all__'


class FullWatchedDetailSerializer(serializers.ModelSerializer):
    """Serializer for FullWatchedShow model (return detail information)"""
    user_link = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = FullWatchedShow
        fields = '__all__'
