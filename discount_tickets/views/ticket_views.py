from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from discount_tickets.helpers import ticket_helper
from discount_tickets.serializers.ticket_serializers import TicketSerializer
from restaurant.helpers import restaurant_helper


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
        restaurant = restaurant_helper.get_restaurant_by_id_and_owner(restaurant_id, request.user.owner)
        tickets = ticket_helper.get_tickets_for_restaurant(restaurant)
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
        restaurant = restaurant_helper.get_restaurant_by_id_and_owner(restaurant_id, request.user.owner)

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
        restaurant = restaurant_helper.get_restaurant_by_id_and_owner(restaurant_id, request.user.owner)
        ticket = ticket_helper.get_ticket_for_restaurant(ticket_id, restaurant)
        if ticket is None:
            return Response("Ticket not found", status=status.HTTP_404_NOT_FOUND)

        serializer = TicketSerializer(ticket, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        responses={
            200: TicketSerializer,
            404: "Ticket not found"
        }
    )
    def put(self, request, restaurant_id, ticket_id):
        restaurant = restaurant_helper.get_restaurant_by_id_and_owner(restaurant_id, request.user.owner)

        ticket = ticket_helper.get_ticket_for_restaurant(ticket_id, restaurant)
        if ticket is None:
            return Response("Ticket not found", status=status.HTTP_404_NOT_FOUND)

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
        restaurant = restaurant_helper.get_restaurant_by_id_and_owner(restaurant_id, request.user.owner)
        ticket = ticket_helper.get_ticket_for_restaurant(ticket_id, restaurant)
        if ticket is None:
            return Response("Ticket not found", status=status.HTTP_404_NOT_FOUND)
        ticket.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)
