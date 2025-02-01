from django.contrib import admin
from django.urls import path, include

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('doctor/', include('doctor.urls')),
    path('administrator/', include('administrator.urls')),
    path('frontdesk/', include('frontdesk.urls')),
    path('pharmacy/', include('pharmacy.urls')),
    path('api/v1/', include('djoser.urls')),
    path('api/v1/', include('djoser.urls.jwt'))
]
