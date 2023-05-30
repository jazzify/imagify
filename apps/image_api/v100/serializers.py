from rest_framework import serializers


class ImageSerializer(serializers.Serializer):
    instance = serializers.ImageField()
