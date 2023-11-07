from restaurant.exceptions.custom_exceptions import RestaurantNotFoundException
from restaurant.models import Owner
from restaurant.models import Restaurant


def get_restaurant_by_id_and_owner(restaurant_id, owner: Owner) -> Restaurant:
    try:
        restaurant = Restaurant.objects.get(id=restaurant_id, owner=owner)
        return restaurant
    except Restaurant.DoesNotExist:
        raise RestaurantNotFoundException(
            f"Restaurant with id {restaurant_id} and owner {owner.user.username} does not exists."
        )


def get_restaurant_by_id(restaurant_id) -> Restaurant:
    try:
        restaurant = Restaurant.objects.get(id=restaurant_id)
        return restaurant
    except Restaurant.DoesNotExist:
        raise RestaurantNotFoundException(f"Restaurant with id {restaurant_id} does not exists.")
