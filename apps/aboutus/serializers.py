from rest_framework import serializers

from .models import AboutUs


class AboutUsSerializer(serializers.ModelSerializer):
    class Meta:
        model = AboutUs
        fields = 'description phone_number instagram mail'.split()
