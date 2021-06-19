from rest_framework import serializers


class LaterWatchShowSerializer(serializers.Serializer):
    myshows_id = serializers.CharField()
    title_eng = serializers.CharField(max_length=100)
    year = serializers.CharField()
