from rest_framework.response import Response
from rest_framework import generics, status, permissions

from apps.reviews.serializers import CompanyReviewSerializer
from apps.reviews.models import CompanyReview
from . import serializers, models


'''Company'''


class CompanyApiView(generics.ListAPIView):
    queryset = models.Company.objects.all()
    serializer_class = serializers.CompanySerializer
    permission_classes = [permissions.AllowAny]


class CompanyDetailApiView(generics.RetrieveAPIView):
    queryset = models.Company.objects.all()
    serializer_class = serializers.CompanyDetailSerializer
    permission_classes = [permissions.AllowAny]

    @staticmethod
    def get_reviews(company, request):
        reviews = CompanyReview.objects.filter(company=company).order_by('-created_at')
        serializer = CompanyReviewSerializer(reviews, many=True, context={'request': request})
        return serializer.data

    def get(self, request, *args, **kwargs):
        company = self.get_object()
        company.views += 1
        company.save()

        reviews = self.get_reviews(company, request)

        company_data = serializers.CompanyDetailSerializer(company, context={'request': request}).data
        company_data['reviews'] = reviews

        return Response(status=status.HTTP_200_OK,
                        data=company_data)


'''Favorite'''


class MakeCompanyFavorite(generics.CreateAPIView):
    serializer_class = serializers.CompanyFavoriteSerializer
    permissions = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        company_id = serializer.validated_data.get('company_id')
        if company_id != self.kwargs['pk']:
            return Response('wrong company id')
        company = models.Company.objects.filter(id=company_id).first()
        if company:
            if not models.FavoriteCompany.objects.filter(user=user, company=company).exists():
                models.FavoriteCompany.objects.create(user=user, company=company)
            else:
                company = models.FavoriteCompany.objects.filter(company=company)
                company.delete()
                return Response(data={'message': 'unfavorite'})
            return Response(status=status.HTTP_200_OK, data={'messsage': 'favorite'})

        return Response(data={'message': 'wrong company'}, status=status.HTTP_400_BAD_REQUEST)
