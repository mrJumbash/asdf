from rest_framework import status
from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from apps.reviews.models import DesignerReview
from apps.reviews.serializers import DesignerReviewSerializer
from .models import Designer, FavoriteDesigner
from . import serializers


class DesignerListApiView(generics.ListAPIView):
    queryset = Designer.objects.all()
    serializer_class = serializers.DesignerSerializer
    permission_classes = [AllowAny]


class DesignerDetailView(generics.RetrieveAPIView):
    queryset = Designer.objects.all()
    serializer_class = serializers.DesignerDetailSerializer
    permission_classes = [AllowAny]

    @staticmethod
    def get_reviews(request, designer):
        reviews = DesignerReview.objects.filter(designer=designer).order_by('-created_at')
        serializer = DesignerReviewSerializer(reviews, many=True, context={'request': request})
        return serializer.data

    def get(self, request, *args, **kwargs):
        designer = self.get_object()
        reviews = self.get_reviews(request, designer)

        designer_data = serializers.DesignerDetailSerializer(designer, context={'request': request}).data
        designer_data['reviews'] = reviews

        return Response(status=status.HTTP_200_OK,
                        data=designer_data)


class MakeDesignerFavorite(generics.CreateAPIView):
    serializer_class = serializers.DesignerFavoriteSerializer
    permissions = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        designer_id = serializer.validated_data.get('designer_id')
        if designer_id != self.kwargs['pk']:
            return Response('wrong designer id')
        designer = Designer.objects.filter(id=designer_id).first()
        if designer:
            if not FavoriteDesigner.objects.filter(user=user, designer=designer).exists():
                FavoriteDesigner.objects.create(user=user, designer=designer)
            else:
                designer = FavoriteDesigner.objects.filter(designer=designer)
                designer.delete()
                return Response(data={'message': 'unfavorite'})
            return Response(status=status.HTTP_200_OK, data={'message': 'favorite'})
        return Response(data={'message': 'wrong designer'}, status=status.HTTP_400_BAD_REQUEST)