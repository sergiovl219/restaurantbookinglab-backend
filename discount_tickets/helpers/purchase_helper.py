from uuid import UUID

from django.db.models import QuerySet

from discount_tickets.exceptions.custom_exceptions import PurchaseNotFoundException
from discount_tickets.models.purchase import Purchase
from restaurant.models.restaurant import Restaurant


def get_purchase_by_id(purchase_id: UUID) -> Purchase:
    """
    Retrieve a specific purchase by its UUID.

    Args:
        purchase_id (UUID): The UUID of the purchase to retrieve.

    Returns:
        Purchase: The Purchase object matching the UUID.

    Raises:
        PurchaseNotFoundException: If the specified purchase is not found.

    """
    try:
        purchase = Purchase.objects.get(id=purchase_id)
        return purchase
    except Purchase.DoesNotExist:
        raise PurchaseNotFoundException(f"Purchase with id {purchase_id} does not exists.")


def get_purchases_by_restaurant(restaurant: Restaurant) -> QuerySet[Purchase]:
    """
    Retrieve a list of purchases for a specific restaurant.

    Args:
        restaurant (Restaurant): The restaurant for which to retrieve purchases.

    Returns:
        QuerySet[Purchase]: A QuerySet of Purchase objects associated with the restaurant's tickets.

    Raises:
        PurchaseNotFoundException: If there are no purchases for the specified restaurant.

    """
    try:
        purchases = Purchase.objects.filter(ticket__restaurant=restaurant)
        return purchases
    except Purchase.DoesNotExist:
        raise PurchaseNotFoundException(f"Purchases for restaurant {restaurant} does not exists.")
