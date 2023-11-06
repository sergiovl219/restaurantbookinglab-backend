from restaurant.models import Owner
from restaurant.models import Restaurant


def get_restaurant_by_id_and_owner(restaurant_id, owner: Owner) -> Restaurant:
    try:
        restaurant = Restaurant.objects.get(id=restaurant_id, owner=owner)
        return restaurant
    except Restaurant.DoesNotExist as e:
        # TODO: Custom Exception
        raise e


def get_restaurant_by_id(restaurant_id) -> Restaurant:
    try:
        restaurant = Restaurant.objects.get(id=restaurant_id)
        return restaurant
    except Restaurant.DoesNotExist as e:
        # TODO: Custom Exception
        raise e
