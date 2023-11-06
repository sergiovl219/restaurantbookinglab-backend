from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from restaurant.models import Owner
from restaurant.models import Restaurant


@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class HomePageView(APIView):
    def get(self, request):
        user = request.user
        # TODO: Move to serializer or helpers
        owner = Owner.objects.get(user=user)
        restaurants = Restaurant.objects.filter(owner=owner)

        user_data = {
            'username': user.username,
            'email': user.email,
        }

        restaurant_data = []
        for restaurant in restaurants:
            restaurant_data.append({
                'name': restaurant.name,
                'url': restaurant.page_url,
            })

        response_data = {
            'user': user_data,
            'restaurants': restaurant_data
        }

        return Response(response_data, status=status.HTTP_200_OK)
