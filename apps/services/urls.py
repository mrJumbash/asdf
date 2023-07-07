from django.urls import path
from . import views

urlpatterns = [
    path('', views.ServicesModelViewSet.as_view()),
]
