from rest_framework import serializers
from .models import Item


class ItemSerializer(serializers.ModelSerializer):
    """Сериализатор модели Item"""
    
    class Meta:
        model = Item
        fields = ('id', 'name', 'description', 'price') 
