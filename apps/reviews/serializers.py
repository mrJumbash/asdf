from datetime import datetime, timedelta
import pytz
from rest_framework import serializers
from .models import CompanyReview, DesignerReview


class CompanyReviewSerializer(serializers.ModelSerializer):
    company = serializers.SerializerMethodField()
    user_photo = serializers.SerializerMethodField()

    class Meta:
        model = CompanyReview
        fields = ('id', 'rank', 'company', 'text', 'user_photo')
        read_only_fields = ('author',)

    def get_company(self, obj):
        if obj.company:
            company_data = {
                'title': obj.company.title,
                'image_url': obj.company.image.url
            }
            request = self.context.get('request')
            if request:
                company_data['image_url'] = request.build_absolute_uri(company_data['image_url'])
            return company_data
        return None

    def get_user_photo(self, instance):
        user = instance.author
        if user and user.image:
            request = self.context.get('request')
            user_photo_url = user.image.url
            if request:
                return request.build_absolute_uri(user_photo_url)
            return user_photo_url
        return None

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        user = instance.author
        representation['username'] = user.username
        representation['first_name'] = user.first_name
        representation['last_name'] = user.last_name
        if 'user_photo' in representation and 'username' in representation and 'first_name' in representation \
                and 'last_name' in representation:
            view = self.context.get('view')
            from apps.reviews.views import UserReviewListView
            if view and isinstance(view, UserReviewListView):
                representation.pop('username')
                representation.pop('first_name')
                representation.pop('last_name')
                representation.pop('user_photo')
        request = self.context.get('request')
        view = self.context.get('view')
        from apps.reviews.views import CompanyReviewList
        if request and view and isinstance(view, CompanyReviewList):
            representation.pop('company', None)

        representation = {key: value for key, value in representation.items() if value}
        hide_company_fields = self.context.get('hide_company_fields', False)
        if hide_company_fields:
            representation.pop('company', None)
        created_at = instance.created_at
        # updated_at = instance.updated_at

        user_timezone = pytz.timezone(user.timezone if user.timezone else 'UTC')
        created_at = created_at.astimezone(user_timezone)

        time_difference = datetime.now(user_timezone) - created_at

        if time_difference < timedelta(days=1):
            hours = int(time_difference.total_seconds() // 3600)
            minutes = int((time_difference.total_seconds() % 3600) // 60)
            representation['time_since_published'] = f"опубликовано {hours} часов {minutes} минут назад"
        elif time_difference < timedelta(days=7):
            days = int(time_difference.days)
            representation['time_since_published'] = f"опубликовано {days} дня назад"
        elif time_difference < timedelta(days=30):
            weeks = int(time_difference.days // 7)
            representation['time_since_published'] = f"опубликовано {weeks} недели назад"
        else:
            months = int(time_difference.days // 30)
            representation['time_since_published'] = f"опубликовано {months} месяца назад"
        return representation

    def update(self, instance, validated_data):
        user = self.context['request'].user
        if instance.author != user:
            raise serializers.ValidationError("Вы не являетесь автором отзыва.")

        instance.rank = validated_data.get('rank', instance.rank)
        instance.text = validated_data.get('text', instance.text)
        instance.save()

        return instance

    def delete(self, instance):
        user = self.context['request'].user
        if instance.author != user:
            raise serializers.ValidationError("Вы не являетесь автором отзыва.")


class DesignerReviewSerializer(serializers.ModelSerializer):
    designer = serializers.SerializerMethodField()
    user_photo = serializers.SerializerMethodField()

    class Meta:
        model = DesignerReview
        fields = ('id', 'rank', 'text', 'user_photo', 'designer')
        read_only_fields = ('author',)

    def get_designer(self, obj):
        if obj.designer:
            designer_data = {
                'name': obj.designer.name,
                'photo_url': obj.designer.photo.url
            }
            request = self.context.get('request')
            if request:
                designer_data['photo_url'] = request.build_absolute_uri(designer_data['photo_url'])
            return designer_data
        return None

    def get_user_photo(self, instance):
        user = instance.author
        if user and user.image:
            request = self.context.get('request')
            user_photo_url = user.image.url
            if request:
                return request.build_absolute_uri(user_photo_url)
            return user_photo_url
        return None

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        user = instance.author
        representation['username'] = user.username
        representation['first_name'] = user.first_name
        representation['last_name'] = user.last_name
        if 'user_photo' in representation and 'username' in representation and 'first_name' in representation \
                and 'last_name' in representation:
            view = self.context.get('view')
            from apps.reviews.views import UserReviewListView
            if view and isinstance(view, UserReviewListView):
                representation.pop('username')
                representation.pop('first_name')
                representation.pop('last_name')
                representation.pop('user_photo')
        request = self.context.get('request')
        view = self.context.get('view')
        from apps.reviews.views import DesignerReviewList
        if request and view and isinstance(view, DesignerReviewList):
            representation.pop('designer', None)
        representation = {key: value for key, value in representation.items() if value}
        hide_company_fields = self.context.get('hide_company_fields', False)
        if hide_company_fields:
            representation.pop('company', None)
            representation.pop('designer', None)
        created_at = instance.created_at
        # updated_at = instance.updated_at

        user_timezone = pytz.timezone(user.timezone if user.timezone else 'UTC')
        created_at = created_at.astimezone(user_timezone)

        time_difference = datetime.now(user_timezone) - created_at

        if time_difference < timedelta(days=1):
            hours = int(time_difference.total_seconds() // 3600)
            minutes = int((time_difference.total_seconds() % 3600) // 60)
            representation['time_since_published'] = f"опубликовано {hours} часов {minutes} минут назад"
        elif time_difference < timedelta(days=7):
            days = int(time_difference.days)
            representation['time_since_published'] = f"опубликовано {days} дня назад"
        elif time_difference < timedelta(days=30):
            weeks = int(time_difference.days // 7)
            representation['time_since_published'] = f"опубликовано {weeks} недели назад"
        else:
            months = int(time_difference.days // 30)
            representation['time_since_published'] = f"опубликовано {months} месяца назад"
        return representation

    def update(self, instance, validated_data):
        user = self.context['request'].user
        if instance.author != user:
            raise serializers.ValidationError("Вы не являетесь автором отзыва.")

        instance.rank = validated_data.get('rank', instance.rank)
        instance.text = validated_data.get('text', instance.text)
        instance.save()

        return instance

    def delete(self, instance):
        user = self.context['request'].user
        if instance.author != user:
            raise serializers.ValidationError("Вы не являетесь автором отзыва.")


class UserReviewsSerializer(serializers.Serializer):

    def get_user_photo(self, instance):
        user = instance.author
        if user and user.image:
            request = self.context.get('request')
            user_photo_url = user.image.url
            if request:
                return request.build_absolute_uri(user_photo_url)
            return user_photo_url
        return None
