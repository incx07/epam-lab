"""Description of the data serialization methods."""

from rest_framework import serializers
from myshowsapp.models import LaterWatchShow, FullWatchedShow


class LaterWatchListSerializer(serializers.ModelSerializer):
    class Meta:
        model = LaterWatchShow
        fields = ['title_eng', 'year']


class LaterWatchDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = LaterWatchShow
        fields = '__all__'


class FullWatchedListSerializer(serializers.ModelSerializer):
    class Meta:
        model = FullWatchedShow
        fields = ['title_eng', 'year']


class FullWatchedDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = FullWatchedShow
        fields = '__all__'
