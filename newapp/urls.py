from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import NewAppViewSet

router = DefaultRouter()

router.register('newapp', NewAppViewSet, basename='newapp')

urlpatterns = [
    path('', include(router.urls))
]