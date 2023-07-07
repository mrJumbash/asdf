from rest_framework import generics
from rest_framework.permissions import AllowAny

from apps.aboutus import serializers
from apps.aboutus.models import AboutUs


class AboutUsListApiView(generics.ListAPIView):
    queryset = AboutUs.objects.all()
    serializer_class = serializers.AboutUsSerializer
    permission_classes = [AllowAny]

