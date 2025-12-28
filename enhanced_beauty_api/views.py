from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Client, Service, Visit, VisitService
from .serializers import ClientSerializer, ServiceSerializer, VisitSerializer, VisitServiceSerializer

class ClientViewSet(viewsets.ModelViewSet):
    serializer_class = ClientSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Client.objects.filter(created_by_user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(created_by_user=self.request.user)

class ServiceViewSet(viewsets.ModelViewSet):
    serializer_class = ServiceSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Service.objects.all()

class VisitViewSet(viewsets.ModelViewSet):
    serializer_class = VisitSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Visit.objects.filter(created_by_user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(created_by_user=self.request.user)

class VisitServiceViewSet(viewsets.ModelViewSet):
    serializer_class = VisitServiceSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return VisitService.objects.filter(visit__created_by_user=self.request.user)
