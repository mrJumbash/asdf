from django.urls import path
from . import views


urlpatterns = [
    # path('', ReviewListCreateView.as_view(), name='review-list-create'),
    # path('<int:pk>/', ReviewRetrieveUpdateDestroyView.as_view(), name='review-retrieve-update-destroy'),

    # company reviews
    path('<int:company_id>/reviews/', views.CompanyReviewList.as_view(), name='company-reviews'),
    path('<int:company_id>/reviews/<int:pk>/', views.CompanyReviewUpdateDestroy.as_view(),
         name='company-review-update-destroy'),

    # reviews_designers
    # path('reviews/', views.DesignerReviewList.as_view(), name='designer-reviews'),
    # path('reviews/<int:pk>/', views.DesignerReviewUpdateDestroy.as_view(),
    #      name='designer-review-update-destroy'),
]

