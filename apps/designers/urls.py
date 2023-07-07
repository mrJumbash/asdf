from django.urls import path

from apps.designers.views import DesignerListApiView, DesignerDetailView, MakeDesignerFavorite
from apps.reviews import views


urlpatterns = [
    # designers
    path('', DesignerListApiView.as_view()),
    path('<int:pk>/', DesignerDetailView.as_view()),

    # designers_reviews
    path('<int:designer_id>/reviews/', views.DesignerReviewList.as_view(), name='designer-reviews'),
    path('<int:designer_id>/reviews/<int:pk>/', views.DesignerReviewUpdateDestroy.as_view(),
         name='designer-review-update-destroy'),

    # favorite
    path('<int:pk>/favorite/', MakeDesignerFavorite.as_view()),
]
