from restaurant.models import Restaurant


def get_restaurant_by_id_and_owner(restaurant_id, owner):
    try:
        restaurant = Restaurant.objects.get(id=restaurant_id, owner=owner)
        return restaurant
    except Restaurant.DoesNotExist:

        return None
