from .models import Services
from .serializers import ServicesSerializers
from rest_framework.permissions import AllowAny
from rest_framework import generics


class ServicesModelViewSet(generics.ListAPIView):
    queryset = Services.objects.all()
    serializer_class = ServicesSerializers
    permission_classes = [AllowAny]




