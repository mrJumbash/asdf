from rest_framework import serializers
from .models import Services


class ServicesSerializers(serializers.ModelSerializer):

    class Meta:
        model = Services
        fields = 'id title description company'.split()


class ServicesValidateSerializers(serializers.Serializer):
    title = serializers.CharField(max_length=100)
    description = serializers.CharField(required=False, default='No description')
