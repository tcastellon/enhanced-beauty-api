from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from enhanced_beauty_api.views import ClientViewSet, ServiceViewSet, VisitViewSet, VisitServiceViewSet

router = DefaultRouter()
router.register(r'clients', ClientViewSet)
router.register(r'services', ServiceViewSet)
router.register(r'visits', VisitViewSet)
router.register(r'visit-services', VisitServiceViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
]
