from celery import shared_task
from django.db import transaction

from discount_tickets.helpers.ticket_helper import get_ticket_by_id
from discount_tickets.serializers.purchase_serializers import PurchaseSerializer


@shared_task
def process_ticket_purchase(creation_data: dict):
    with transaction.atomic():
        serializer = PurchaseSerializer(data=creation_data)
        serializer.is_valid(raise_exception=True)
        ticket = get_ticket_by_id(creation_data["ticket"])
        try:
            serializer.save(ticket=ticket, guest=None)
            return serializer.data
        except Exception as e:
            raise e
