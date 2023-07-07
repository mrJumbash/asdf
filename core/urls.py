from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from core.settings import swagger
from apps.aboutus.views import AboutUsListApiView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    # users
    path('api/v1/users/', include('apps.users.urls')),
    # companies
    path('api/v1/companies/', include('apps.companies.urls')),
    # designers
    path('api/v1/designers/', include('apps.designers.urls')),
    # services
    path('api/v1/services/', include('apps.services.urls')),
    # about us
    path('api/v1/aboutus/', AboutUsListApiView.as_view()),
    # admin
    path('api/v1/admin/', include('apps.admin_panel.urls')),
    # token
    path('api/v1/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/v1/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/v1/token/verify/', TokenVerifyView.as_view(), name='token_verify'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += swagger.urlpatterns
