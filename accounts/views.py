import secrets
import bcrypt

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from django.contrib.auth import authenticate, login

from .models import CustomUser, CustomToken
from .serializers import CustomUserSerializer, LoginSerializer
from .authentication import expired_token_handler, expires_in

class UserViewSet(viewsets.ViewSet):

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
    def token_generator(self, user):
        """function to generate a bcrypted token"""
        key = bcrypt.hashpw(secrets.token_hex(50).encode('utf-8'), bcrypt.gensalt())
        key = key.decode('utf-8')
        token, _ = CustomToken.objects.update_or_create(user=user, defaults={'key': key})
        return token

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

        try:
            token = CustomToken.objects.get(user=user)
            is_expired, token = expired_token_handler(token)
            if is_expired:
                token = self.token_generator(user)
        except CustomToken.DoesNotExist:
            token = self.token_generator(user)

        authenticated_user = CustomUserSerializer(user)
        return Response(
            {
                "message": "Login successful",
                "user": authenticated_user.data,
                "token": token.key,
                'code': 200
            },
            status=status.HTTP_200_OK
        )

class LogoutViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]
    def create(self, request):
        token = request.headers.get('Authorization')
        try:
            token = CustomToken.objects.get(key=token)
            token.delete()
        except CustomToken.DoesNotExist:
            return Response(
                {"message": "Invalid token", 'code': 400},
                status=status.HTTP_400_BAD_REQUEST
            )
        return Response(
            {"message": "Logout successful", 'code': 200},
            status=status.HTTP_200_OK
        )