from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response

from .models import NewApp
from .serializers import NewAppSerializer

class NewAppViewSet(viewsets.ViewSet):
    def create(self, request):
        serializer = NewAppSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'data': serializer.data, 'code': 200}, status=status.HTTP_201_CREATED)
        return Response({'data': serializer.errors, 'code': 400}, status=status.HTTP_400_BAD_REQUEST)
