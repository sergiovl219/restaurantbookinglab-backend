from django.contrib.auth.models import User

from restaurant.exceptions.custom_exceptions import OwnerNotFoundException
from restaurant.models import Owner


def get_owner_by_user(user: User) -> Owner:
    """
    Get the owner associated with the given User.

    Args:
        user (User): The User object to look up an associated Owner for.

    Returns:
        Owner: The Owner associated with the User.

    Raises:
        OwnerNotFoundException: If no Owner is found for the given User.

    """
    try:
        return Owner.objects.get(user=user)
    except Owner.DoesNotExist:
        raise OwnerNotFoundException(f"Owner linked to user {user.username} not found")
