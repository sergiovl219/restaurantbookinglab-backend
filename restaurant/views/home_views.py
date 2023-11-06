from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from restaurant.helpers import owner_helper
from restaurant.serializers.owner_serializers import OwnerDataSerializer


@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class HomePageView(APIView):
    @swagger_auto_schema(
        responses={
            200: OwnerDataSerializer,
            400: "Owner not found"
        }
    )
    def get(self, request):
        user = request.user
        owner = owner_helper.get_owner_by_user(user)

        if owner is not None:
            serializer = OwnerDataSerializer(owner)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response("Owner not found", status=status.HTTP_404_NOT_FOUND)
