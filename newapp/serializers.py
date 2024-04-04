from rest_framework import serializers
from .models import NewApp

class NewAppSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewApp
        fields = '__all__'