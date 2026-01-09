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
        queryset = Visit.objects.filter(created_by_user=self.request.user)

        client_id = self.request.query_params.get('client_id', None)
        if client_id is not None:
            queryset = queryset.filter(client_id=client_id)

        return queryset

    def perform_create(self, serializer):
        serializer.save(created_by_user=self.request.user)

class VisitServiceViewSet(viewsets.ModelViewSet):
    serializer_class = VisitServiceSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = VisitService.objects.filter(visit__created_by_user=self.request.user)
        visit_id = self.request.query_params.get('visit_id', None)

        if visit_id is not None:
            queryset = queryset.filter(visit_id=visit_id)

        return queryset

    def perform_create(self, serializer):
        serializer.save()
