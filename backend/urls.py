from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from enhanced_beauty_api.views import ClientViewSet, ServiceViewSet, VisitViewSet, VisitServiceViewSet, AvailabilityViewSet, BookingViewSet, register, login, chat

router = DefaultRouter()
router.register(r'clients', ClientViewSet, 'client')
router.register(r'services', ServiceViewSet, 'service')
router.register(r'visits', VisitViewSet, 'visit')
router.register(r'visitservices', VisitServiceViewSet, 'visitservice')
router.register(r'availability', AvailabilityViewSet, 'availability')
router.register(r'booking', BookingViewSet, 'booking')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/login/', login, name='api_token_auth'),
    path('api/register/', register, name='api_register'),
    path('api/chat/', chat, name='api_chat')
]
