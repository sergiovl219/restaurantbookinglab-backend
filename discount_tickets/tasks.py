from celery import shared_task

from discount_tickets.helpers.ticket_helper import get_ticket_by_id
from discount_tickets.serializers.purchase_serializers import PurchaseSerializer


@shared_task
def process_ticket_purchase(creation_data):
    pass
