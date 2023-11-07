from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from restaurant.exceptions.api_exceptions import OwnerNotFoundAPIException
from restaurant.exceptions.custom_exceptions import OwnerNotFoundException
from restaurant.helpers import owner_helper
from restaurant.serializers.owner_serializers import OwnerDataSerializer
from restaurantbookinglab.exceptions import BadRequestAPIException


@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class UserInfoView(APIView):
    @swagger_auto_schema(
        responses={
            200: OwnerDataSerializer,
            400: "Owner not found"
        }
    )
    def get(self, request):
        """
        Get owner information.

        Retrieves owner information associated with the authenticated user account.

        Args:
            request (HttpRequest): The HTTP request.

        Returns:
            Response: A response containing owner information.

        Raises:
            OwnerNotFoundAPIException: If the owner is not found.
            BadRequestAPIException: If an unexpected error occurs.

        """
        user = request.user
        try:
            owner = owner_helper.get_owner_by_user(user)
        except OwnerNotFoundException as e:
            raise OwnerNotFoundAPIException(e.message)
        except Exception:
            raise BadRequestAPIException

        serializer = OwnerDataSerializer(owner)
        return Response(serializer.data, status=status.HTTP_200_OK)
