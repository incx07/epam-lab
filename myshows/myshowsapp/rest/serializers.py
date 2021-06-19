from rest_framework import serializers
from myshowsapp.models import LaterWatchShow


class LaterWatchListSerializer(serializers.ModelSerializer):
    class Meta:
        model = LaterWatchShow
        fields = ['title_eng', 'year']


class LaterWatchDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = LaterWatchShow
        fields = '__all__'
