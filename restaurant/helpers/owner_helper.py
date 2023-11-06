from restaurant.models import Owner


def get_owner_by_user(user):
    try:
        return Owner.objects.get(user=user)
    except Owner.DoesNotExist:
        # TODO: Raise custom exception
        return None
