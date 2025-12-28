from rest_framework import serializers
from .models import Client, Service, Visit, VisitService

class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = '__all__'
        read_only_fields = ['created_by_user', 'created_at', 'updated_at']

class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = '__all__'

class VisitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Visit
        fields = '__all__'
        read_only_fields = ['created_by_user', 'created_at', 'updated_at']

class VisitServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = VisitService
        fields = '__all__'
        read_only_fields = ['created_at']
