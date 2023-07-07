from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from apps.designers.models import Designer, DesignerGallery
from apps.aboutus.models import AboutUs
from apps.services.models import Services
from apps.companies.models import Company


"""Designers CompanyGallery"""


class DGSerializerAdmin(serializers.ModelSerializer):
    class Meta:
        model = DesignerGallery
        fields = 'id image about designer_id'.split()

    image = serializers.ImageField()
    about = serializers.CharField(max_length=50, default='')
    designer_id = serializers.IntegerField()

    @staticmethod
    def validate_designer_id(designer_id):
        try:
            Designer.objects.get(id=designer_id)
        except Designer.DoesNotExist:
            raise ValidationError(f'Director with id ({designer_id}) not found')
        return designer_id


"""Designers"""


class DesignerSerializerAdmin(serializers.ModelSerializer):
    class Meta:
        model = Designer
        fields = '__all__'

    name = serializers.CharField(max_length=30)
    surname = serializers.CharField(max_length=30)
    photo = serializers.ImageField()
    work_EXP = serializers.CharField(max_length=50, required=False)
    occupation = serializers.CharField(max_length=25)
    description = serializers.CharField(required=False)
    phone_number = serializers.CharField(max_length=15)
    email = serializers.EmailField()
    instagram = serializers.URLField(required=False)


"""About us"""


class AboutUsSerializerAdmin(serializers.ModelSerializer):
    class Meta:
        model = AboutUs
        fields = '__all__'

    image = serializers.ImageField()
    description = serializers.CharField()
    phone_number = serializers.CharField(max_length=20)
    instagram = serializers.URLField()
    mail = serializers.EmailField()


"""Services"""


class ServiceSerializerAdmin(serializers.ModelSerializer):
    class Meta:
        model = Services
        fields = '__all__'

    image = serializers.ImageField(required=False)
    title = serializers.CharField(max_length=100)
    description = serializers.CharField(required=False)


""" Company """


class CompanyAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ['id', 'image', 'title', 'summary', 'services', 'packages',
                  'views', 'rating', 'count_reviews']


class CompanyDetailAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = '__all__'
