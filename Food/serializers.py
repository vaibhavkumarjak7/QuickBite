from rest_framework import serializers
from .models import Item,Order
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
        
    def validate(self, data):
        if data["item_name"].lower() == data["item_desc"].lower():
            raise serializers.ValidationError("Item name and description must not be same")
        return data
        
class OrderSerializer(serializers.ModelSerializer):
    items = ItemSerializer(many=True,read_only=True)
    user = serializers.StringRelatedField()
    class Meta:
        model = Order
        fields = ["id","user","ordered_at","items"]