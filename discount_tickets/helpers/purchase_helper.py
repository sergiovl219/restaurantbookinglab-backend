from typing import List

from django.db.models import QuerySet

from discount_tickets.models.purchase import Purchase
from restaurant.models.restaurant import Restaurant


def get_purchase_by_id(purchase_id) -> Purchase:
    try:
        purchase = Purchase.objects.get(id=purchase_id)
        return purchase
    except Purchase.DoesNotExist as e:
        # TODO: Custom exceptions
        raise e


def get_purchases_by_restaurant(restaurant: Restaurant) -> QuerySet[Purchase]:
    try:
        purchases = Purchase.objects.filter(ticket__restaurant=restaurant)
        return purchases
    except Purchase.DoesNotExist as e:
        # TODO: Custom exceptions
        raise e
