import random as rand
from django.contrib.auth import authenticate
from rest_framework import generics, status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from django.core.mail import EmailMessage
from django.conf import settings
from apps.users import serializers, models
from apps.companies.models import FavoriteCompany
from rest_framework import permissions
from apps.designers.models import FavoriteDesigner



class RegisterUser(generics.CreateAPIView):
    serializer_class = serializers.RegisterSerializer
    permission_classes = [permissions.AllowAny]
    host_user = 'settings.EMAIL_HOST_USER'

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        password = serializer.validated_data.get('password')
        password2 = serializer.validated_data.get('password2')
        if password != password2:
            user.delete()
            return Response('Пароли не совпадают')
        email = serializer.validated_data.get('email')
        try:
            code = models.ConfirmCode.objects.create(username=user.username, code=rand.randint(10000, 100000))
        except:
            code = models.ConfirmCode.objects.get(username=user.username)
            code.delete()
            code = models.ConfirmCode.objects.create(username=user.username, code=rand.randint(10000, 100000))

        send_email = EmailMessage("Confirmation code", f'Пожалуйста введите этот код подтверждения \n {str(code.code)}',
                                  from_email=self.host_user, to=[email])
        if send_email.send():
            return Response(data={f'confirmation email send to {email}, Check your spam folder'},
                            status=status.HTTP_201_CREATED)
        user.delete()
        return Response(data={f'Problem sending email to {email}, check if you typed it correctly'},
                        status=status.HTTP_400_BAD_REQUEST)


class ConfirmationUser(generics.GenericAPIView):
    serializer_class = serializers.ConfirmSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        code = serializer.validated_data.get('code')
        confirm = get_object_or_404(models.ConfirmCode, code=code)
        username = confirm.username
        user = models.User.objects.get(username=username)
        user.is_active = True
        user.save()
        confirm.delete()
        refresh = RefreshToken.for_user(user)
        access = AccessToken.for_user(user)
        return Response(data={'status': 'User confirmed!',
                              'refresh_token': str(refresh),
                              'access_token': str(access),
                              'expires_in': str(access.lifetime)})


class ResendConfirmCode(generics.GenericAPIView):
    serializer_class = serializers.ResendConfirmCodeSerializer
    permission_classes = [permissions.AllowAny]
    host_user = 'settings.EMAIL_HOST_USER'

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data.get('username')
        try:
            code = models.ConfirmCode.objects.get(username=username)
        except models.ConfirmCode.DoesNotExist:
            return Response(data={'Wrong username'}, status=status.HTTP_400_BAD_REQUEST)
        code.delete()
        user = models.User.objects.filter(username=username).first()
        code = models.ConfirmCode.objects.create(username=user.username, code=rand.randint(10000, 100000))
        send_email = EmailMessage("Код подтверждения", f'Пожалуйста введите этот код подтверждения \n {str(code.code)}',
                                  from_email=self.host_user, to=[user.email])
        if send_email.send():
            return Response(data={f'confirmation email resend to {user.email}, Check your spam folder'},
                            status=status.HTTP_201_CREATED)
        return Response(data={f'Problem sending email to {user.email}, check if you typed it correctly'},
                        status=status.HTTP_400_BAD_REQUEST)


class Login(generics.GenericAPIView):
    serializer_class = serializers.LoginSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = authenticate(**serializer.validated_data)
        if user:
            refresh = RefreshToken.for_user(user)
            access = AccessToken.for_user(user)
            return Response(
                {
                    'user': user.username,
                    'token': str(refresh),
                    'access_token': str(access),
                    'expires_in': str(access.lifetime)
                }
            )
        return Response(data={'Неправильный логин или пароль!'}, status=status.HTTP_401_UNAUTHORIZED)


class ChangePassword(generics.GenericAPIView):
    serializer_class = serializers.ChangePasswordSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def patch(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        if not user.check_password(serializer.data.get("old_password")):
            return Response({"old_password": ["Неправильный пароль"]}, status=status.HTTP_400_BAD_REQUEST)
        new_password = serializer.validate_password(serializer.validated_data.get('new_password'))
        new_password2 = serializer.validated_data.get('new_password2')
        if new_password != new_password2:
            return Response(data={'message': 'Пароли не совпали'}, status=status.HTTP_400_BAD_REQUEST)
        user.set_password(new_password)
        user.save()
        return Response(
            data={'message': 'Пароль успешно изменён!'},
            status=status.HTTP_200_OK
        )


class ResetPassword(generics.GenericAPIView):
    serializer_class = serializers.ResetPasswordSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validate_email(serializer.validated_data.get('email'))
        user = models.User.objects.filter(email=email).first()
        if user:
            code = models.ResetPasswordCode.objects.create(email=email, code=rand.randint(10000, 100000))
            send_email = EmailMessage(subject='Сброс пароля', body=f'Пожалуйста введите этот код для сброса пароля \n'
                                                                   f'{str(code.code)}',
                                      from_email=settings.EMAIL_HOST_USER, to=[email])
            if send_email.send():
                return Response(data={f'confirmation email send to {user.email}, Check your spam folder'},
                                status=status.HTTP_201_CREATED)
            return Response(data={f'Problem sending email to {user.email}, check if you typed it correctly'},
                            status=status.HTTP_400_BAD_REQUEST)
        return Response('wrong email', status=status.HTTP_400_BAD_REQUEST)


class ResendResetCode(generics.GenericAPIView):
    serializer_class = serializers.ResendResetCodeSerializer
    permission_classes = [permissions.AllowAny]
    host_user = 'settings.EMAIL_HOST_USER'

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data.get('email')
        try:
            code = models.ResetPasswordCode.objects.get(email=email)
        except models.ResetPasswordCode.DoesNotExist:
            return Response(data={'Wrong email'}, status=status.HTTP_400_BAD_REQUEST)
        code.delete()
        user = models.User.objects.filter(email=email).first()
        code = models.ResetPasswordCode.objects.create(email=user.email, code=rand.randint(10000, 100000))
        send_email = EmailMessage("Reset Password code", f'Пожалуйста введите этот код для сброса пароля \n '
                                                         f'{str(code.code)}',
                                  from_email=self.host_user, to=[user.email])
        if send_email.send():
            return Response(data={f'reset password email resend to {user.email}, Check your spam folder'},
                            status=status.HTTP_201_CREATED)
        return Response(data={f'Problem sending email to {user.email}, check if you typed it correctly'},
                        status=status.HTTP_400_BAD_REQUEST)


class PasswordResetConfirm(generics.GenericAPIView):
    serializer_class = serializers.ResetPasswordConfirmSerializer
    model = models.ResetPasswordCode
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        code = serializer.validated_data.get('code')
        new_password = serializer.validate_password(serializer.validated_data.get('new_password'))
        new_password2 = serializer.validated_data.get('new_password2')
        reset_password_code = models.ResetPasswordCode.objects.get(code=code)
        if new_password != new_password2:
            return Response('Пароли не совпадают')
        try:
            email = reset_password_code.email
        except reset_password_code.DoesNotExist:
            return Response('Wrong code', status=status.HTTP_400_BAD_REQUEST)
        user = models.User.objects.filter(email=email).first()
        if user:
            user.set_password(new_password)
            user.save()
            models.ResetPasswordCode.objects.filter(code=code).delete()
            return Response(data={'status': 'ok'})
        return Response('wrong', status.HTTP_400_BAD_REQUEST)


class UserProfile(generics.GenericAPIView):
    queryset = models.User.objects.all()
    serializer_class = serializers.UserValidateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def get(self, request, *args, **kwargs):
        user = self.get_object()
        queryset = models.User.objects.get(username=user.username)
        serializer = serializers.UserProfileSerializer(queryset, context={'request': request})
        return Response(serializer.data)

    def put(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        models.User.objects.update(**serializer.validated_data)
        return Response(data={'message : updated successfully'}, status=status.HTTP_200_OK)


class UsersApiView(generics.ListAPIView):
    queryset = models.User.objects.all()
    serializer_class = serializers.UserDetailSerializer
    permission_classes = [permissions.AllowAny]


class UserDetailApiView(generics.RetrieveAPIView):
    queryset = models.User.objects.all()
    serializer_class = serializers.UserDetailSerializer
    permission_classes = [permissions.AllowAny]


class FavoritesApiView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = serializers.FavoriteCompaniesSerializer

    def list(self, request, *args, **kwargs):
        user = self.request.user
        company_favorite = FavoriteCompany.objects.filter(user=user)
        designer_favorite = FavoriteDesigner.objects.filter(user=user)
        serializer_company_favorite = serializers.FavoriteCompaniesSerializer(company_favorite, many=True)
        serializer_designer_favorite = serializers.FavoriteDesignersSerializer(designer_favorite, many=True)

        data = {
            'companies': serializer_company_favorite.data,
            'designers': serializer_designer_favorite.data,
        }
        return Response(data)


class UpdateUserImage(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = serializers.UpdateUserImageSerializer

    def patch(self, request, *args, **kwargs):
        user = self.request.user
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        image = serializer.validated_data.get('image')
        user.image = image
        user.save()
        return Response(
            data={'message': 'Image update successfully'},
            status=status.HTTP_200_OK
        )
