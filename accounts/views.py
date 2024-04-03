from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from django.contrib.auth import authenticate, login

from .models import CustomUser
from .serializers import CustomUserSerializer, LoginSerializer

class UserViewSet(viewsets.ViewSet):
    # permission_classes = [IsAuthenticated]

    def list(self, request):
        queryset = CustomUser.objects.all()
        serializer = CustomUserSerializer(queryset, many=True)
        if not serializer.data:
            return Response(
                {"message": "No users found", 'code': 200},
                status=status.HTTP_200_OK
            )

        return Response(
            {"message": "fetch successful", 'data': serializer.data, 'code': 200},
            status=status.HTTP_200_OK
        )

    def create(self, request):
        email = request.data.get('email')
        if CustomUser.objects.filter(email = email).exists():
            return Response({"message": "User already exists", 'code': 400}, status=status.HTTP_400_BAD_REQUEST)
        serializer = CustomUserSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(
                {"message": serializer.errors, 'code': 400},
                status=status.HTTP_400_BAD_REQUEST
            )
        validated_data = serializer.validated_data
        CustomUser.objects.create_user(**validated_data)
        return Response(
            {"message": "User created successfully", 'code': 201},
            status=status.HTTP_201_CREATED
        )

class LoginViewSet(viewsets.ViewSet):
    def create(self, request):
        serializer = LoginSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                {"message": serializer.errors, 'code': 400},
                status=status.HTTP_400_BAD_REQUEST
            )
        user = authenticate(
            email=serializer.validated_data['email'],
            password=serializer.validated_data['password']
        )
        if not user:
            return Response(
                {"message": "Invalid credentials", 'code': 400},
                status=status.HTTP_400_BAD_REQUEST
            )
        print(user)
        if login(request, user):
            return Response(
                {"message": "Login successful", 'code': 200},
                status=status.HTTP_200_OK)

        return Response(
            {"message": "Login failed", 'code': 400},
            status=status.HTTP_400_BAD_REQUEST
        )
