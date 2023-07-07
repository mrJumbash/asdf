import re
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.validators import UniqueValidator
from apps.designers.models import FavoriteDesigner
from apps.designers.serializers import DesignerSerializer
from apps.users.models import *
from apps.companies.serializers import CompanySerializer
from apps.companies.models import FavoriteCompany


class RegisterSerializer(serializers.Serializer):
    image = serializers.ImageField(required=False, default='user_photo/default.jpg')
    username = serializers.CharField(min_length=4)
    email = serializers.EmailField(required=True, validators=[UniqueValidator(queryset=User.objects.all())])
    password = serializers.CharField(min_length=8)
    password2 = serializers.CharField(min_length=8)

    @staticmethod
    def validate_username(username):
        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            return username
        raise ValidationError('User already exists!')

    @staticmethod
    def validate_password(password):
        if re.match("^(?=.*?[a-z])(?=.*?[0-9]).{8,}$", password):
            return password
        raise ValidationError("The password must consist of at least letters and numbers!")

    def create(self, validated_data):
        username = validated_data.get('username')
        password = validated_data.get('password')
        email = validated_data.get('email')
        image = validated_data.get('image')
        user = User.objects.create_user(username=username, password=password, image=image, email=email)
        user.is_active = False
        user.save()
        return user


class ConfirmSerializer(serializers.Serializer):
    code = serializers.IntegerField()

    def validate(self, code):
        try:
            ConfirmCode.objects.filter(code=code)
        except ConfirmCode.DoesNotExist:
            raise ValidationError('Wrong code')
        return code


class ResendConfirmCodeSerializer(serializers.Serializer):
    username = serializers.CharField(min_length=4)


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField()
    new_password = serializers.CharField()
    new_password2 = serializers.CharField()

    @staticmethod
    def validate_password(new_password):
        if re.match("^(?=.*?[a-z])(?=.*?[0-9]).{8,}$", new_password):
            return new_password
        raise ValidationError("Пароль должен содержать хотя-бы цифры и буквы, не менее 8 символов")


class ResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate(self, email):
        try:
            User.objects.filter(email=email)
        except User.DoesNotExist:
            raise ValidationError('Wrong email')
        return email

    @staticmethod
    def validate_email(email):
        try:
            code = ResetPasswordCode.objects.filter(email=email)
        except ResetPasswordCode.DoesNotExist:
            return email
        code.delete()
        return email


class ResendResetCodeSerializer(serializers.Serializer):
    email = serializers.EmailField()


class ResetPasswordConfirmSerializer(serializers.Serializer):
    code = serializers.CharField(max_length=6)
    new_password = serializers.CharField(min_length=8)
    new_password2 = serializers.CharField(min_length=8)

    @staticmethod
    def validate_code(code):
        try:
            ResetPasswordCode.objects.get(code=code)
        except ResetPasswordCode.DoesNotExist:
            raise ValidationError('Wrong code!')
        return code

    @staticmethod
    def validate_password(new_password):
        if re.match("^(?=.*?[a-z])(?=.*?[0-9]).{8,}$", new_password):
            return new_password
        raise ValidationError("The password must consist of at least letters and numbers!")


class UserValidateSerializer(serializers.Serializer):
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)
    about_me = serializers.CharField(required=False)
    image = serializers.ImageField(required=False)


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = 'id image first_name last_name about_me username email'.split()


class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = 'id image first_name last_name about_me username'.split()


class FavoriteCompaniesSerializer(CompanySerializer):
    company = CompanySerializer()

    class Meta:
        model = FavoriteCompany
        fields = 'company'.split()


class FavoriteDesignersSerializer(CompanySerializer):
    designer = DesignerSerializer()

    class Meta:
        model = FavoriteDesigner
        fields = 'designer'.split()


class UpdateUserImageSerializer(serializers.Serializer):
    image = serializers.ImageField(use_url=True)