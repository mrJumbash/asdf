from django.urls import path, include

from apps.companies import views


urlpatterns = [
    path('', views.CompanyApiView.as_view()),
    path('<int:pk>/', views.CompanyDetailApiView.as_view()),

    # company reviews
    path('', include('apps.reviews.urls')),

    # favorite
    path('<int:pk>/favorite/', views.MakeCompanyFavorite.as_view()),

]
