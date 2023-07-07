from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework import status, generics

from apps.companies import models, serializers
from apps.designers.models import Designer, DesignerGallery
from apps.aboutus.models import AboutUs
from apps.services.models import Services
from apps.admin_panel.serializers import DGSerializerAdmin, DesignerSerializerAdmin, ServiceSerializerAdmin, \
    AboutUsSerializerAdmin, CompanyAdminSerializer, CompanyDetailAdminSerializer
from apps.admin_panel.services import DesignerService

"""Designers"""


class DesignerAdminListView(generics.ListCreateAPIView):
    queryset = DesignerService.get_list()
    serializer_class = DesignerSerializerAdmin
    permission_classes = [IsAdminUser]


class DesignerAdminDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Designer.objects.all()
    serializer_class = DesignerSerializerAdmin
    permission_classes = [IsAdminUser]


"""Designers CompanyGallery"""


class DGAdminListView(generics.ListCreateAPIView):
    queryset = DesignerGallery.objects.all()
    serializer_class = DGSerializerAdmin
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        designer_id = self.kwargs['designer_id']
        return DesignerGallery.objects.filter(designer=designer_id)


class DGAdminDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = DesignerGallery.objects.all()
    serializer_class = DGSerializerAdmin
    permission_classes = [IsAdminUser]


"""About us"""


class AboutUsAdminListView(generics.ListCreateAPIView):
    queryset = AboutUs.objects.all()
    serializer_class = AboutUsSerializerAdmin
    permission_classes = [IsAdminUser]


class AboutUsAdminDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = AboutUs.objects.all()
    serializer_class = AboutUsSerializerAdmin
    permission_classes = [IsAdminUser]


"""Services"""


class ServicesAdminListView(generics.ListCreateAPIView):
    queryset = Services.objects.all()
    serializer_class = ServiceSerializerAdmin
    permission_classes = [IsAdminUser]


class ServicesAdminDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Services.objects.all()
    serializer_class = ServiceSerializerAdmin
    permission_classes = [IsAdminUser]


'''Company'''


class CompanyAdminApiView(generics.ListCreateAPIView):
    queryset = models.Company.objects.all()
    permission_classes = [IsAdminUser]

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return CompanyAdminSerializer
        elif self.request.method == 'POST':
            return CompanyDetailAdminSerializer

    def post(self, request, *args, **kwargs):
        serializer = serializers.CompanyValidateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        company = serializer.save()

        return Response(data=serializers.CompanySerializer(company).data,
                        status=status.HTTP_201_CREATED)


class CompanyDetailAdminApiView(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Company.objects.all()
    serializer_class = CompanyDetailAdminSerializer
    permission_classes = [IsAdminUser]

    def put(self, request, *args, **kwargs):
        company = self.get_object()

        serializer = serializers.CompanyDetailSerializer(company, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(status=status.HTTP_200_OK,
                        data=serializers.CompanyDetailSerializer(company).data)


# company gallery
class CompanyGalleryListView(generics.ListCreateAPIView):
    serializer_class = serializers.GallerySerializer
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        companies_id = self.kwargs['companies_id']
        return models.CompanyGallery.objects.filter(company_id=companies_id)


class CompanyGalleryDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.CompanyGallery.objects.all()
    serializer_class = serializers.GallerySerializer
    permission_classes = [IsAdminUser]


# packages
class CompanyPackageAdminAPIView(generics.ListCreateAPIView):
    queryset = models.Package.objects.all()
    serializer_class = serializers.PackageSerializer
    permission_classes = [IsAdminUser]


class CompanyPackageDetailAdminAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Package.objects.all()
    serializer_class = serializers.PackageSerializer
    permission_classes = [IsAdminUser]
