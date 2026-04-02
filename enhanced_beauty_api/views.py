from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.utils import timezone
from .models import Client, Service, Visit, VisitService
from .serializers import (
    ClientSerializer,
    ServiceSerializer,
    VisitSerializer,
    VisitServiceSerializer,
)


@api_view(["POST"])
@permission_classes([AllowAny])
def login(request):
    username = request.data.get("username")
    password = request.data.get("password")

    if not username or not password:
        return Response(
            {"detail": "Username and password are required."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    user = authenticate(username=username, password=password)

    if user is None:
        return Response(
            {"detail": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED
        )

    user.last_login = timezone.now()
    user.save()

    token, _ = Token.objects.get_or_create(user=user)

    return Response(
        {
            "token": token.key,
            "user": {
                "first_name": user.first_name,
                "last_name": user.last_name,
                "username": user.username,
            },
        }
    )


@api_view(["POST"])
@permission_classes([AllowAny])
def register(request):
    username = request.data.get("username")
    email = request.data.get("email")
    password = request.data.get("password")
    first_name = request.data.get("first_name", "")
    last_name = request.data.get("last_name", "")

    if not username or not email or not password:
        return Response(
            {"detail": "Username, email, and password are required."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    if User.objects.filter(username=username).exists():
        return Response(
            {"username": ["A user with this username already exists."]},
            status=status.HTTP_400_BAD_REQUEST,
        )

    if User.objects.filter(email=email).exists():
        return Response(
            {"email": ["A user with this email already exists."]},
            status=status.HTTP_400_BAD_REQUEST,
        )

    try:
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
        )

        user.is_staff = True
        user.save()

        token, _ = Token.objects.get_or_create(user=user)

        return Response(
            {
                "message": "User created successfully",
                "token": token.key,
                "user_id": user.id,
                "username": user.username,
            },
            status=status.HTTP_201_CREATED,
        )

    except Exception as e:
        return Response(
            {"detail": "Failed to create user"}, status=status.HTTP_400_BAD_REQUEST
        )


class ClientViewSet(viewsets.ModelViewSet):
    serializer_class = ClientSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Client.objects.filter(created_by_user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(created_by_user=self.request.user)


class ServiceViewSet(viewsets.ModelViewSet):
    serializer_class = ServiceSerializer

    def get_permissions(self):
        if self.action == 'list':
            return [AllowAny()]
        return [IsAuthenticated()]
    
    def get_queryset(self):
        return Service.objects.all()


class VisitViewSet(viewsets.ModelViewSet):
    serializer_class = VisitSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Visit.objects.filter(created_by_user=self.request.user)

        client_id = self.request.query_params.get("client_id", None)
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
        visit_id = self.request.query_params.get("visit_id", None)

        if visit_id is not None:
            queryset = queryset.filter(visit_id=visit_id)

        return queryset

    def perform_create(self, serializer):
        serializer.save()
