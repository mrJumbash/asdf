import re
from rest_framework import serializers

from apps.designers.serializers import DesignerSerializer
from apps.services.models import Services
from apps.companies import models


class PackageSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(required=True)
    title = serializers.CharField(required=True, max_length=100)
    description = serializers.CharField(required=False)
    price = serializers.CharField(max_length=20, required=False)
    tag = serializers.CharField(max_length=20, required=False)

    class Meta:
        model = models.Package
        fields = '__all__'


class GallerySerializer(serializers.ModelSerializer):
    image = serializers.ImageField(max_length=None, use_url=True, required=True)

    class Meta:
        model = models.CompanyGallery
        fields = ['id', 'company', 'image']


class ServicesSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(read_only=True)
    title = serializers.CharField(max_length=100, required=True)
    description = serializers.CharField(required=False)

    class Meta:
        model = Services
        fields = ['id', 'image', 'title', 'description']


# main page
class CompanySerializer(serializers.ModelSerializer):
    services = ServicesSerializer(many=True)
    packages = PackageSerializer(many=True)

    class Meta:
        model = models.Company
        fields = ['id', 'image', 'title', 'summary', 'services', 'packages',
                  'views', 'rating', 'count_reviews']


class CompanyValidateSerializer(serializers.Serializer):
    image = serializers.ImageField(required=True)
    title = serializers.CharField(max_length=100, required=True)
    summary = serializers.CharField(max_length=255, required=True)
    about = serializers.CharField(required=True)
    phone_number_1 = serializers.CharField(max_length=16, required=True)
    phone_number_2 = serializers.CharField(max_length=16, required=False)
    phone_number_3 = serializers.CharField(max_length=16, required=False)
    email_1 = serializers.EmailField(required=True)
    email_2 = serializers.EmailField(required=False)
    email_3 = serializers.EmailField(required=False)
    social_media_1 = serializers.URLField(required=False)
    social_media_2 = serializers.URLField(required=False)
    social_media_3 = serializers.URLField(required=False)
    social_media_4 = serializers.URLField(required=False)
    address = serializers.CharField(max_length=255, required=True)
    site_link = serializers.URLField(required=True)
    packages = serializers.PrimaryKeyRelatedField(queryset=models.Package.objects.all(), many=True, required=False)
    services = serializers.PrimaryKeyRelatedField(queryset=models.Services.objects.all(), many=True, required=False)
    designers = serializers.PrimaryKeyRelatedField(queryset=models.Designer.objects.all(), many=True, required=False)

    def validate(self, attrs):
        attrs = super().validate(attrs)

        phone_number_1 = attrs.get('phone_number_1')
        phone_number_2 = attrs.get('phone_number_2')
        phone_number_3 = attrs.get('phone_number_3')

        pattern = r'^\+?\d{1,3}?[-.\s]?\(?\d{1,3}?\)?[-.\s]?\d{1,4}[-.\s]?\d{1,4}[-.\s]?\d{1,9}$'

        if phone_number_1 and not re.match(pattern, phone_number_1):
            raise serializers.ValidationError('Invalid phone number format for phone_number_1')

        if phone_number_2 and not re.match(pattern, phone_number_2):
            raise serializers.ValidationError('Invalid phone number format for phone_number_2')

        if phone_number_3 and not re.match(pattern, phone_number_3):
            raise serializers.ValidationError('Invalid phone number format for phone_number_3')

        return attrs

    def create(self, validated_data):
        packages = validated_data.pop('packages', [])
        services = validated_data.pop('services', [])
        designers = validated_data.pop('designers', [])
        company = models.Company.objects.create(**validated_data)
        company.packages.set(packages)
        company.services.set(services)
        company.designers.set(designers)

        return company

    def update(self, instance, validated_data):
        packages = validated_data.pop('packages')
        services = validated_data.pop('services')
        designers = validated_data.pop('designers')

        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.packages.set(packages)
        instance.services.set(services)
        instance.designers.set(designers)
        instance.save()

        return instance


# detail page
class CompanyDetailSerializer(CompanySerializer):
    gallery = GallerySerializer(many=True)
    packages = PackageSerializer(many=True)
    designers = DesignerSerializer(many=True)
    services = ServicesSerializer(many=True)

    class Meta:
        model = models.Company
        fields = ['site_link', 'image', 'title', 'summary', 'about', 'services', 'gallery', 'packages',
                  'designers', 'count_reviews', 'reviews', 'rating', 'phone_number_1', 'phone_number_2',
                  'phone_number_3', 'email_1', 'email_2', 'email_3', 'social_media_1', 'social_media_2',
                  'social_media_3', 'social_media_4', 'address']


class CompanyFavoriteSerializer(serializers.Serializer):
    company_id = serializers.IntegerField()
