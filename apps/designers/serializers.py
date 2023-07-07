from rest_framework import serializers
from .models import Designer, DesignerGallery


class DesignerGallerySerializer(serializers.ModelSerializer):
    class Meta:
        model = DesignerGallery
        fields = 'about image'.split()


class DesignerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Designer
        fields = 'id photo name occupation rating count_reviews'.split()


class DesignerDetailSerializer(serializers.ModelSerializer):
    gallery = DesignerGallerySerializer(many=True)

    class Meta:
        model = Designer
        fields = 'name surname photo  company_title work_EXP occupation description phone_number email instagram ' \
                 'gallery rating count_reviews'.split()


class DesignerFavoriteSerializer(serializers.Serializer):
    designer_id = serializers.IntegerField()
