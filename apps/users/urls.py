from django.urls import path
from apps.reviews.views import UserReviewListView
from apps.users.views import *

urlpatterns = [
    path('', UsersApiView.as_view()),
    path('login/', Login.as_view()),
    path('register/', RegisterUser.as_view()),
    path('confirm/', ConfirmationUser.as_view()),
    path('change_password/', ChangePassword.as_view()),
    path('password_reset/', ResetPassword.as_view()),
    path('password_reset/confirm', PasswordResetConfirm.as_view()),
    path('profile/', UserProfile.as_view()),
    path('<int:pk>/', UserDetailApiView.as_view()),
    path('resend_confirm_code/', ResendConfirmCode.as_view()),
    path('resend_reset_code/', ResendResetCode.as_view()),
    path('myreviews/', UserReviewListView.as_view(), name='user_reviews'),
    path('favorite/', FavoritesApiView.as_view()),
    path('update_image/', UpdateUserImage.as_view())

]