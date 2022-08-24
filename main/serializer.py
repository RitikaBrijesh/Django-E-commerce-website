from dataclasses import field
from rest_framework import serializers
from .models import CartOrderItems

class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model=CartOrderItems
        fields="__all__"

        
