from uuid import UUID

from restaurant.exceptions.custom_exceptions import RestaurantNotFoundException
from restaurant.models import Owner
from restaurant.models import Restaurant


def get_restaurant_by_id_and_owner(restaurant_id: UUID, owner: Owner) -> Restaurant:
    """
    Get a restaurant by its ID and owner.

    Retrieves a restaurant by its ID and the associated owner.

    Args:
        restaurant_id (UUID): The ID of the restaurant to retrieve.
        owner (Owner): The owner associated with the restaurant.

    Returns:
        Restaurant: The restaurant associated with the specified ID and owner.

    Raises:
        RestaurantNotFoundException: If the restaurant with the specified ID and owner does not exist.

    """
    try:
        restaurant = Restaurant.objects.get(id=restaurant_id, owner=owner)
        return restaurant
    except Restaurant.DoesNotExist:
        raise RestaurantNotFoundException(
            f"Restaurant with id {restaurant_id} and owner {owner.user.username} does not exists."
        )


def get_restaurant_by_id(restaurant_id: UUID) -> Restaurant:
    """
     Get a restaurant by its ID.

     Retrieves a restaurant by its ID.

     Args:
         restaurant_id (UUID): The ID of the restaurant to retrieve.

     Returns:
         Restaurant: The restaurant associated with the specified ID.

     Raises:
         RestaurantNotFoundException: If the restaurant with the specified ID does not exist.

     """
    try:
        restaurant = Restaurant.objects.get(id=restaurant_id)
        return restaurant
    except Restaurant.DoesNotExist:
        raise RestaurantNotFoundException(f"Restaurant with id {restaurant_id} does not exists.")
