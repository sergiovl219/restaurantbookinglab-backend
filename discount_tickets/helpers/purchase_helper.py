from django.db.models import QuerySet

from discount_tickets.exceptions.custom_exceptions import PurchaseNotFoundException
from discount_tickets.models.purchase import Purchase
from restaurant.models.restaurant import Restaurant


def get_purchase_by_id(purchase_id) -> Purchase:
    try:
        purchase = Purchase.objects.get(id=purchase_id)
        return purchase
    except Purchase.DoesNotExist:
        raise PurchaseNotFoundException(f"Purchase with id {purchase_id} does not exists.")


def get_purchases_by_restaurant(restaurant: Restaurant) -> QuerySet[Purchase]:
    try:
        purchases = Purchase.objects.filter(ticket__restaurant=restaurant)
        return purchases
    except Purchase.DoesNotExist:
        raise PurchaseNotFoundException(f"Purchases for restaurant {restaurant} does not exists.")
