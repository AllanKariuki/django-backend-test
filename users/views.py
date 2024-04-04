from rest_framework import viewsets, status
from rest_framework.response import Response

from .models import UserData
from .serializers import UserDataSerializer

class UserDataViewSet(viewsets.ViewSet):
    def create(self, request):
        serializer = UserDataSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'data': serializer.data, 'code':200}, status=status.HTTP_201_CREATED)
        return Response({'data': serializer.errors, 'code': 400}, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request):
        print(request.user)
        user = request.data.get('user')
        try:
            user_data = UserData.objects.filter(user=user)
        except UserData.DoesNotExist:
            return Response({'data': 'Profile not found', 'code': 404}, status=status.HTTP_404_NOT_FOUND)
        serializer = UserDataSerializer(user_data, many=True)
        return Response({'data': serializer.data, 'code': 200}, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        try:
            user_data = UserData.objects.get(pk=pk)
        except UserData.DoesNotExist:
            return Response({'data': 'Profile not found', 'code': 404}, status=status.HTTP_404_NOT_FOUND)
        serializer = UserDataSerializer(user_data)
        return Response({'data': serializer.data, 'code': 200}, status=status.HTTP_200_OK)

    def update(self, request, pk=None):
        try:
            user_data = UserData.objects.get(pk=pk)
        except UserData.DoesNotExist:
            return Response({'data': 'Profile not found', 'code': 404}, status=status.HTTP_404_NOT_FOUND)
        serializer = UserDataSerializer(user_data, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'data': serializer.data, 'code': 200}, status=status.HTTP_200_OK)
        return Response({'data': serializer.errors, 'code': 400}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        UserData.objects.get(pk=pk).delete()
        return Response({'data': 'Profile deleted', 'code': 200}, status=status.HTTP_200_OK)
