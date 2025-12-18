from rest_framework import serializers
from .models import Client, Service, Visit, VisitService

class ClientSerializers(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = '__all__'

class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = '__all__'

class VisitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Visit
        fields = '__all__'

class VisitServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = VisitService
        fields = '__all__'
