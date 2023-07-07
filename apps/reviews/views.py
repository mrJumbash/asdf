from rest_framework import generics, permissions
from rest_framework.response import Response
from apps.reviews.models import CompanyReview, DesignerReview
from apps.reviews.serializers import CompanyReviewSerializer, DesignerReviewSerializer, UserReviewsSerializer


class IsReviewAuthor(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.author == request.user


class CompanyReviewList(generics.ListCreateAPIView):
    serializer_class = CompanyReviewSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        company_id = self.kwargs['company_id']
        return CompanyReview.objects.filter(company_id=company_id).order_by('-created_at')

    def perform_create(self, serializer):
        company_id = self.kwargs['company_id']
        serializer.save(author=self.request.user, company_id=company_id)


class CompanyReviewUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CompanyReviewSerializer
    permission_classes = [permissions.IsAuthenticated, IsReviewAuthor]

    def get_queryset(self):
        company_id = self.kwargs['company_id']
        return CompanyReview.objects.filter(company_id=company_id, author=self.request.user)


class DesignerReviewList(generics.ListCreateAPIView):
    serializer_class = DesignerReviewSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        designer_id = self.kwargs['designer_id']
        return DesignerReview.objects.filter(designer_id=designer_id).order_by('-created_at')

    def perform_create(self, serializer):
        designer_id = self.kwargs['designer_id']
        serializer.save(author=self.request.user, designer_id=designer_id)


class DesignerReviewUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = DesignerReviewSerializer
    permission_classes = [permissions.IsAuthenticated, IsReviewAuthor]

    def get_queryset(self):
        designer_id = self.kwargs['designer_id']
        return DesignerReview.objects.filter(author=self.request.user, designer_id=designer_id)


class UserReviewListView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserReviewsSerializer

    def list(self, request, *args, **kwargs):
        user = self.request.user
        company_reviews = CompanyReview.objects.filter(author=user).order_by('-created_at')
        designer_reviews = DesignerReview.objects.filter(author=user).order_by('-created_at')
        serializer_company_reviews = CompanyReviewSerializer(company_reviews, many=True)
        serializer_designer_reviews = DesignerReviewSerializer(designer_reviews, many=True)

        total_company_reviews = company_reviews.count()
        total_designer_reviews = designer_reviews.count()
        total_reviews = total_company_reviews + total_designer_reviews

        data = {
            'total_reviews': total_reviews,
            'company_reviews': serializer_company_reviews.data,
            'designer_reviews': serializer_designer_reviews.data,
        }

        data.pop('first_name', None)
        data.pop('last_name', None)
        data.pop('user_photo', None)

        return Response(data)
