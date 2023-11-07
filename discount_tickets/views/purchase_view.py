from django.db import transaction
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import authentication_classes
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response

from discount_tickets import tasks
from discount_tickets.exceptions.api_exceptions import PurchaseNotFoundAPIException
from discount_tickets.exceptions.api_exceptions import TicketNotFoundAPIException
from discount_tickets.exceptions.custom_exceptions import PurchaseNotFoundException
from discount_tickets.exceptions.custom_exceptions import TicketNotFoundException
from discount_tickets.helpers import purchase_helper
from discount_tickets.helpers import ticket_helper
from discount_tickets.serializers.purchase_serializers import PurchaseSerializer
from discount_tickets.serializers.purchase_serializers import PurchaseTicketQueuedSerializer
from discount_tickets.serializers.purchase_serializers import PurchaseTicketSerializer
from restaurant.exceptions.api_exceptions import OwnerNotFoundAPIException
from restaurant.exceptions.api_exceptions import RestaurantNotFoundAPIException
from restaurant.exceptions.custom_exceptions import OwnerNotFoundException
from restaurant.exceptions.custom_exceptions import RestaurantNotFoundException
from restaurant.helpers import owner_helper
from restaurant.helpers import restaurant_helper
from restaurantbookinglab.exceptions import BadRequestAPIException


@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class TicketPurchaseGetView(APIView):
    @swagger_auto_schema(
        responses={
            200: PurchaseSerializer,
            400: "Bad Request"
        }
    )
    def get(self, request, restaurant_id, purchase_id):
        """
        Retrieve the details of a purchase ticket for a restaurant.

        Args:
            request: The request object.
            restaurant_id (UUID): The ID of the restaurant.
            purchase_id (UUID): The ID of the purchase.

        Returns:
            Response: A Response object with the details of the purchase or an error message.

        Raises:
            OwnerNotFoundAPIException: If the owner is not found.
            RestaurantNotFoundAPIException: If the restaurant is not found.
            PurchaseNotFoundAPIException: If the purchase is not found.
            BadRequestAPIException: If an unexpected error occurs.

        """
        try:
            owner = owner_helper.get_owner_by_user(request.user)
            restaurant = restaurant_helper.get_restaurant_by_id_and_owner(restaurant_id, owner)
            purchase = purchase_helper.get_purchase_by_id(purchase_id)
        except OwnerNotFoundException as e:
            raise OwnerNotFoundAPIException(e.message)
        except RestaurantNotFoundException as e:
            raise RestaurantNotFoundAPIException(e.message)
        except PurchaseNotFoundException as e:
            raise PurchaseNotFoundAPIException(e.message)
        except Exception:
            raise BadRequestAPIException

        serializer = PurchaseSerializer(purchase, many=False)

        return Response(serializer.data, status=status.HTTP_200_OK)


class TicketPurchaseCreateView(APIView):
    authentication_classes = []

    @swagger_auto_schema(
        request_body=PurchaseTicketSerializer,
        responses={
            201: PurchaseTicketQueuedSerializer,
            400: "Ticket not available",
            409: "Not enough tickets available"
        }
    )
    def post(self, request, restaurant_id, ticket_id):
        """
        Create a new purchase for a ticket at a restaurant. Celery task added.

        Args:
            request: The request object.
            restaurant_id (UUID): The ID of the restaurant.
            ticket_id (UUID): The ID of the ticket.

        Returns:
            Response: A Response object with the details of the created purchase or an error message.

        Raises:
            RestaurantNotFoundAPIException: If the restaurant is not found.
            TicketNotFoundAPIException: If the ticket is not found.
            BadRequestAPIException: If an unexpected error occurs.

        """
        serializer = PurchaseTicketSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            restaurant = restaurant_helper.get_restaurant_by_id(restaurant_id)
            ticket = ticket_helper.get_ticket_for_restaurant(ticket_id, restaurant)
        except RestaurantNotFoundException as e:
            raise RestaurantNotFoundAPIException(e.message)
        except TicketNotFoundException as e:
            raise TicketNotFoundAPIException(e.message)
        except Exception as e:
            raise BadRequestAPIException(e.__str__())

        with transaction.atomic():
            if ticket.count <= 0:
                return Response("Ticket not available", status=status.HTTP_400_BAD_REQUEST)

            serializer = PurchaseTicketSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            quantity = serializer.validated_data['quantity']
            if quantity > ticket.count:
                return Response("Not enough tickets available", status=status.HTTP_400_BAD_REQUEST)

            creation_data = {
                "ticket": ticket.id,
                "guest": None,  # TODO: Pending to define
                "quantity": quantity
            }

            task = tasks.process_ticket_purchase.apply_async(args=(creation_data,))
            serializer_response = PurchaseTicketQueuedSerializer(data={"task_id": task.id})
            serializer_response.is_valid(raise_exception=True)
            return Response(
                serializer_response.validated_data,
                status=status.HTTP_202_ACCEPTED
            )


@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class TicketPurchaseListView(APIView):
    @swagger_auto_schema(
        responses={
            200: PurchaseSerializer(many=True),
            400: "Ticket not available",
            409: "Not enough tickets available"
        }
    )
    def get(self, request, restaurant_id):
        """
        Retrieve a list of ticket purchases for a specific restaurant.

        Args:
            request: The request object.
            restaurant_id (UUID): The ID of the restaurant.

        Returns:
            Response: A Response object containing a list of purchases for the restaurant or an error message.

        Raises:
            OwnerNotFoundAPIException: If the owner is not found.
            RestaurantNotFoundAPIException: If the restaurant is not found.
            PurchaseNotFoundAPIException: If no purchases are found.
            BadRequestAPIException: If an unexpected error occurs.

        """
        try:
            owner = owner_helper.get_owner_by_user(request.user)
            restaurant = restaurant_helper.get_restaurant_by_id_and_owner(restaurant_id, owner)
            purchases = purchase_helper.get_purchases_by_restaurant(restaurant)
        except OwnerNotFoundException as e:
            raise OwnerNotFoundAPIException(e.message)
        except RestaurantNotFoundException as e:
            raise RestaurantNotFoundAPIException(e.message)
        except PurchaseNotFoundException as e:
            raise PurchaseNotFoundAPIException(e.message)
        except Exception:
            raise BadRequestAPIException
        serializer = PurchaseSerializer(purchases, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
