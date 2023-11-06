from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from discount_tickets.models import Ticket
from discount_tickets.serializers.ticket_serializers import TicketSerializer
from restaurant.helpers import restaurant_helper
from restaurant.models import Restaurant


@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class ListTicketsView(APIView):
    @swagger_auto_schema(
        responses={
            200: TicketSerializer,
        }
    )
    def get(self, request, restaurant_id):
        restaurant = restaurant_helper.get_restaurant_by_id_and_owner(restaurant_id, request.user.owner)

        tickets = Ticket.objects.filter(restaurant=restaurant)
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
        }
    )
    def get(self, request, restaurant_id, ticket_id):
        restaurant = restaurant_helper.get_restaurant_by_id_and_owner(restaurant_id, request.user.owner)

        try:
            ticket = Ticket.objects.get(id=ticket_id, restaurant=restaurant)
        except Ticket.DoesNotExist:
            return Response("Ticket not found", status=status.HTTP_404_NOT_FOUND)

        serializer = TicketSerializer(ticket, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        responses={
            200: TicketSerializer,
        }
    )
    def put(self, request, restaurant_id, ticket_id):
        restaurant = restaurant_helper.get_restaurant_by_id_and_owner(restaurant_id, request.user.owner)

        try:
            ticket = Ticket.objects.get(id=ticket_id, restaurant=restaurant)
        except Ticket.DoesNotExist:
            return Response("Ticket not found", status=status.HTTP_404_NOT_FOUND)

        # Actualiza el ticket
        serializer = TicketSerializer(ticket, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        responses={
            204: "",
        }
    )
    def delete(self, request, restaurant_id, ticket_id):
        restaurant = restaurant_helper.get_restaurant_by_id_and_owner(restaurant_id, request.user.owner)

        # Obtén el ticket y elimínalo
        try:
            ticket = Ticket.objects.get(id=ticket_id, restaurant=restaurant)
            ticket.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Ticket.DoesNotExist:
            return Response("Ticket not found", status=status.HTTP_404_NOT_FOUND)
