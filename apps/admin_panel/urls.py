from django.urls import path
from . import views


urlpatterns = [
    # designers
    path('designers/', views.DesignerAdminListView.as_view()),
    path('designers/<int:pk>/', views.DesignerAdminDetailView.as_view()),

    # designers gallery
    path('designers/<int:designer_id>/gallery/', views.DGAdminListView.as_view()),
    path('designers/gallery/<int:pk>/', views.DGAdminDetailView.as_view()),

    # about us
    path('aboutus/', views.AboutUsAdminListView.as_view()),
    path('aboutus/<int:pk>/', views.AboutUsAdminDetailView.as_view()),

    # services
    path('services/', views.ServicesAdminListView.as_view()),
    path('services/<int:pk>/', views.ServicesAdminDetailView.as_view()),

    # companies
    path('companies/', views.CompanyAdminApiView.as_view()),
    path('companies/<int:pk>/', views.CompanyDetailAdminApiView.as_view()),

    # companies gallery
    path('companies/<int:companies_id>/gallery/', views.CompanyGalleryListView.as_view()),
    path('companies/gallery/<int:pk>/', views.CompanyGalleryDetailView.as_view()),

    # packages
    path('packages/', views.CompanyPackageAdminAPIView.as_view()),
    path('packages/<int:pk>/', views.CompanyPackageDetailAdminAPIView.as_view())
]
