from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from discount_tickets.exceptions.api_exceptions import TicketNotFoundAPIException
from discount_tickets.exceptions.custom_exceptions import TicketNotFoundException
from discount_tickets.helpers import ticket_helper
from discount_tickets.serializers.ticket_serializers import TicketSerializer
from restaurant.exceptions.api_exceptions import RestaurantNotFoundAPIException
from restaurant.exceptions.custom_exceptions import RestaurantNotFoundException
from restaurant.helpers import restaurant_helper
from restaurantbookinglab.exceptions import BadRequestAPIException


@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class ListTicketsView(APIView):
    @swagger_auto_schema(
        responses={
            200: TicketSerializer,
            400: "Bad Request"
        }
    )
    def get(self, request, restaurant_id):
        """
        Get a list of tickets for a restaurant.

        Args:
            request: The request object.
            restaurant_id (UUID): The ID of the restaurant.

        Returns:
            Response: A Response object with the list of tickets or an error message.

        Raises:
            RestaurantNotFoundAPIException: If the restaurant is not found.
            BadRequestAPIException: If an unexpected error occurs.

        """
        try:
            restaurant = restaurant_helper.get_restaurant_by_id_and_owner(restaurant_id, request.user.owner)
            tickets = ticket_helper.get_tickets_for_restaurant(restaurant)
        except RestaurantNotFoundException as e:
            raise RestaurantNotFoundAPIException(e.message)
        except Exception:
            raise BadRequestAPIException

        serializer = TicketSerializer(tickets, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class CreateTicketView(APIView):
    @swagger_auto_schema(
        request_body=TicketSerializer,
        responses={
            200: TicketSerializer,
            400: "Owner not found"
        }
    )
    def post(self, request, restaurant_id):
        """
        Create a new ticket for a restaurant.

        Args:
            request: The request object.
            restaurant_id (UUID): The ID of the restaurant.

        Returns:
            Response: A Response object with the created ticket or an error message.

        Raises:
            RestaurantNotFoundAPIException: If the restaurant is not found.
            BadRequestAPIException: If an unexpected error occurs.

        """
        try:
            restaurant = restaurant_helper.get_restaurant_by_id_and_owner(restaurant_id, request.user.owner)
        except RestaurantNotFoundException as e:
            raise RestaurantNotFoundAPIException(e.message)
        except Exception:
            raise BadRequestAPIException

        serializer = TicketSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(restaurant=restaurant)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class RUDTicketView(APIView):
    @swagger_auto_schema(
        responses={
            200: TicketSerializer,
            404: "Ticket not found"
        }
    )
    def get(self, request, restaurant_id, ticket_id):
        """
        Get the details of a ticket for a restaurant.

        Args:
            request: The request object.
            restaurant_id (UUID): The ID of the restaurant.
            ticket_id (UUID): The ID of the ticket.

        Returns:
            Response: A Response object with the details of the ticket or an error message.

        Raises:
            RestaurantNotFoundAPIException: If the restaurant is not found.
            TicketNotFoundAPIException: If the ticket is not found.
            BadRequestAPIException: If an unexpected error occurs.

        """
        try:
            restaurant = restaurant_helper.get_restaurant_by_id_and_owner(restaurant_id, request.user.owner)
            ticket = ticket_helper.get_ticket_for_restaurant(ticket_id, restaurant)
        except RestaurantNotFoundException as e:
            raise RestaurantNotFoundAPIException(e.message)
        except TicketNotFoundException as e:
            raise TicketNotFoundAPIException(e.message)
        except Exception:
            raise BadRequestAPIException

        serializer = TicketSerializer(ticket, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        responses={
            200: TicketSerializer,
            404: "Ticket not found"
        }
    )
    def put(self, request, restaurant_id, ticket_id):
        """
        Update the details of a ticket for a restaurant.

        Args:
            request: The request object.
            restaurant_id (UUID): The ID of the restaurant.
            ticket_id (UUID): The ID of the ticket.

        Returns:
            Response: A Response object with the updated ticket details or an error message.

        Raises:
            RestaurantNotFoundAPIException: If the restaurant is not found.
            TicketNotFoundAPIException: If the ticket is not found.
            BadRequestAPIException: If an unexpected error occurs.

        """
        try:
            restaurant = restaurant_helper.get_restaurant_by_id_and_owner(restaurant_id, request.user.owner)
            ticket = ticket_helper.get_ticket_for_restaurant(ticket_id, restaurant)
        except RestaurantNotFoundException as e:
            raise RestaurantNotFoundAPIException(e.message)
        except TicketNotFoundException as e:
            raise TicketNotFoundAPIException(e.message)
        except Exception:
            raise BadRequestAPIException

        serializer = TicketSerializer(ticket, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        responses={
            204: "",
            404: "Ticket not found"
        }
    )
    def delete(self, request, restaurant_id, ticket_id):
        """
        Delete a ticket for a restaurant.

        Args:
            request: The request object.
            restaurant_id (UUID): The ID of the restaurant.
            ticket_id (UUID): The ID of the ticket.

        Returns:
            Response: A Response object with a success status or an error message.

        Raises:
            RestaurantNotFoundAPIException: If the restaurant is not found.
            TicketNotFoundAPIException: If the ticket is not found.
            BadRequestAPIException: If an unexpected error occurs.

        """
        try:
            restaurant = restaurant_helper.get_restaurant_by_id_and_owner(restaurant_id, request.user.owner)
            ticket = ticket_helper.get_ticket_for_restaurant(ticket_id, restaurant)
            ticket.delete()
        except RestaurantNotFoundException as e:
            raise RestaurantNotFoundAPIException(e.message)
        except TicketNotFoundException as e:
            raise TicketNotFoundAPIException(e.message)
        except Exception:
            raise BadRequestAPIException

        return Response(status=status.HTTP_204_NO_CONTENT)
