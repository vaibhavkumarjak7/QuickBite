from rest_framework import serializers
from .models import Item
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id","username","email"]

class ItemSerializer(serializers.ModelSerializer):
    user_name = UserSerializer(read_only=True)
    class Meta:
        model = Item
        fields = ["id","user_name","item_name","item_desc","item_price","item_image"]
        
    def validate_item_price(self,value):
        if value<0:
            raise serializers.ValidationError("Price must be positive")
        return value
        