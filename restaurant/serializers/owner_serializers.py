from rest_framework import serializers

from .restaurant_serializers import RestaurantSerializer
from ..models import Owner


class UserOwnerSerializer(serializers.ModelSerializer):
    username = serializers.CharField()
    email = serializers.EmailField()

    class Meta:
        model = Owner
        fields = [
            'username',
            'email'
        ]


class OwnerDataSerializer(serializers.Serializer):
    owner = UserOwnerSerializer(
        source="user"
    )
    restaurants_info = RestaurantSerializer(
        source="restaurants",
        many=True
    )
