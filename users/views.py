from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import UserData
from .serializers import UserDataSerializer

class UserDataViewSet(viewsets.ViewSet):
    # permission_classes = [IsAuthenticated]
    def create(self, request):
        serializer = UserDataSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'data': 'Added successfully', 'code':200}, status=status.HTTP_201_CREATED)
        return Response({'data': serializer.errors, 'code': 400}, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request):
        user = request.data.get('user')
        try:
            # user_data = UserData.objects.filter(user=user)
            user_data = UserData.objects.all()
        except UserData.DoesNotExist:
            return Response({'data': 'Profile not found', 'code': 404}, status=status.HTTP_404_NOT_FOUND)
        serializer = UserDataSerializer(user_data, many=True)
        print(user_data)
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

