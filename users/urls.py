from django.urls import path, include
from rest_framework import routers
from .views import UserDataViewSet

router = routers.DefaultRouter()

router.register(r'userdata', UserDataViewSet, basename='users')

urlpatterns = [
    path('', include(router.urls)),
    # path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]