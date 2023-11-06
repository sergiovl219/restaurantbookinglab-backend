from django.contrib.auth.models import User

from restaurant.models import Owner


def get_owner_by_user(user: User):
    try:
        return Owner.objects.get(user=user)
    except Owner.DoesNotExist:
        # TODO: Raise custom exception
        return None
