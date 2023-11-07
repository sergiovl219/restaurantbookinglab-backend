from uuid import UUID

from discount_tickets.exceptions.custom_exceptions import TicketNotFoundException
from discount_tickets.models.ticket import Ticket
from restaurant.models import Restaurant


def get_tickets_for_restaurant(restaurant: Restaurant):
    """
    Retrieve a list of tickets for a specific restaurant.

    Args:
        restaurant (Restaurant): The restaurant for which to retrieve tickets.

    Returns:
        QuerySet: A QuerySet of Ticket objects associated with the restaurant.

    Raises:
        None

    """
    tickets = Ticket.objects.filter(restaurant=restaurant)
    return tickets


def get_ticket_for_restaurant(ticket_id: UUID, restaurant: Restaurant) -> Ticket:
    """
    Retrieve a specific ticket for a restaurant by its ID.

    Args:
        ticket_id (UUID): The ID of the ticket to retrieve.
        restaurant (Restaurant): The restaurant to which the ticket belongs.

    Returns:
        Ticket: The Ticket object matching the ID and restaurant.

    Raises:
        TicketNotFoundException: If the specified ticket is not found for the given restaurant.

    """
    try:
        ticket = Ticket.objects.get(id=ticket_id, restaurant=restaurant)
        return ticket
    except Ticket.DoesNotExist:
        raise TicketNotFoundException(f"Ticket {ticket_id} not found for restaurant {restaurant}")


def get_ticket_by_id(ticket_id: UUID) -> Ticket:
    """
    Retrieve a specific ticket by its ID.

    Args:
        ticket_id (UUID): The ID of the ticket to retrieve.

    Returns:
        Ticket: The Ticket object matching the ID.

    Raises:
        TicketNotFoundException: If the specified ticket is not found.

    """
    try:
        ticket = Ticket.objects.get(id=ticket_id)
        return ticket
    except Ticket.DoesNotExist:
        raise TicketNotFoundException(f"Ticket {ticket_id} not found")


def update_ticket_count(ticket: Ticket, amount: int):
    """
    Update the count of available tickets for a specific ticket.

    Args:
        ticket (Ticket): The ticket to update.
        amount (int): The amount to subtract from the ticket's count.

    Returns:
        None

    Raises:
        None

    """
    ticket.count -= amount
    ticket.save()
