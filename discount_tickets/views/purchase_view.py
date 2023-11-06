import logging

from django.db import transaction
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import authentication_classes
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response

from discount_tickets.helpers import purchase_helper
from discount_tickets.helpers import ticket_helper
from discount_tickets.models import Ticket
from discount_tickets.serializers.purchase_serializers import PurchaseSerializer
from discount_tickets.serializers.purchase_serializers import PurchaseTicketSerializer
from restaurant.helpers import owner_helper
from restaurant.helpers import restaurant_helper


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
        owner = owner_helper.get_owner_by_user(request.user)
        restaurant = restaurant_helper.get_restaurant_by_id_and_owner(restaurant_id, owner)
        purchase = purchase_helper.get_purchase_by_id(purchase_id)
        serializer = PurchaseSerializer(purchase, many=False)

        return Response(serializer.data, status=status.HTTP_200_OK)


class TicketPurchaseCreateView(APIView):
    @swagger_auto_schema(
        request_body=PurchaseTicketSerializer,
        responses={
            201: PurchaseSerializer,
            400: "Ticket not available",
            409: "Not enough tickets available"
        }
    )
    def post(self, request, restaurant_id, ticket_id):
        restaurant = restaurant_helper.get_restaurant_by_id(restaurant_id)
        ticket = ticket_helper.get_ticket_for_restaurant(ticket_id, restaurant)

        if ticket.count <= 0:
            return Response("Ticket not available", status=status.HTTP_400_BAD_REQUEST)

        serializer = PurchaseTicketSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        quantity = serializer.validated_data['quantity']
        if quantity > ticket.count:
            return Response("Not enough tickets available", status=status.HTTP_400_BAD_REQUEST)

        with transaction.atomic():
            creation_data = {
                "ticket": ticket.id,
                "guest": None,  # TODO: Pending to define
                "quantity": quantity
            }
            serializer = PurchaseSerializer(data=creation_data)
            if serializer.is_valid():
                # TODO: Catch Exception and Raise API Exception
                serializer.save(ticket=ticket, guest=None)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
        owner = owner_helper.get_owner_by_user(request.user)
        restaurant = restaurant_helper.get_restaurant_by_id_and_owner(restaurant_id, owner)
        purchases = purchase_helper.get_purchases_by_restaurant(restaurant)
        serializer = PurchaseSerializer(purchases, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
