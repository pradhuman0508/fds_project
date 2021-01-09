"""deviceproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from .router import router
from rest_framework_simplejwt import views as jwt_views
from device import views as device_views



urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/device/auth/start/', device_views.NewDeviceView.as_view(), name='new_device'),
    path('api/device/last-seen/', device_views.DeviceLastSeenView.as_view(), name='device_last-seen'),
    path('api/device/last-seen/update/',device_views.DeviceLastSeenUpdateView.as_view(),name='device_last-seen_update'),
    path('api/device/auth/check/',device_views.DeviceTokenView.as_view(),name='device_check_view'),
    path('api/device/key-exchange/',device_views.DeviceKeyExchangeView.as_view(),name='device-key_exchange'),
    path('api/device/auth/reauth/',device_views.DeviceReauthenticateView.as_view(),name='device-'),
    path('api/device/details/',device_views.DeviceDetailsView.as_view(),name='device_details')

]
from django.conf import settings
from django.conf.urls.static import static
if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)