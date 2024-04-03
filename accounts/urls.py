from django.urls import path, include
from .views import UserViewSet, LoginViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('signup', UserViewSet, basename='users')
router.register('login', LoginViewSet, basename='login')

urlpatterns = [
    path('', include(router.urls)),
    ]