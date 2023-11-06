import logging

from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from restaurant.models import Owner
from restaurant.models import Restaurant
from restaurant.serializers.owner_serializers import OwnerDataSerializer
from restaurant.serializers.owner_serializers import UserOwnerSerializer
from restaurant.serializers.restaurant_serializers import RestaurantSerializer


@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class HomePageView(APIView):
    @swagger_auto_schema(
        responses={
            200: OwnerDataSerializer
        }
    )
    def get(self, request):
        user = request.user
        owner = Owner.objects.get(user=user)
        serializer = OwnerDataSerializer(owner)

        return Response(serializer.data, status=status.HTTP_200_OK)
