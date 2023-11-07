from django.contrib.auth.models import User

from restaurant.exceptions.custom_exceptions import OwnerNotFoundException
from restaurant.models import Owner


def get_owner_by_user(user: User):
    try:
        return Owner.objects.get(user=user)
    except Owner.DoesNotExist:
        raise OwnerNotFoundException(f"Owner linked to user {user.username} not found")
