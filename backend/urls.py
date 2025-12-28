from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token
from enhanced_beauty_api.views import ClientViewSet, ServiceViewSet, VisitViewSet, VisitServiceViewSet

router = DefaultRouter()
router.register(r'clients', ClientViewSet, 'client')
router.register(r'services', ServiceViewSet, 'service')
router.register(r'visits', VisitViewSet, 'visit')
router.register(r'visit-services', VisitServiceViewSet, 'visitservice')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/login/', obtain_auth_token, name='api_token_auth')
]
