from discount_tickets.exceptions.custom_exceptions import TicketNotFoundException
from discount_tickets.models.ticket import Ticket
from restaurant.models import Restaurant


def get_tickets_for_restaurant(restaurant: Restaurant):
    tickets = Ticket.objects.filter(restaurant=restaurant)
    return tickets


def get_ticket_for_restaurant(ticket_id, restaurant: Restaurant) -> Ticket:
    try:
        ticket = Ticket.objects.get(id=ticket_id, restaurant=restaurant)
        return ticket
    except Ticket.DoesNotExist:
        raise TicketNotFoundException(f"Ticket {ticket_id} not found for restaurant {restaurant}")


def get_ticket_by_id(ticket_id) -> Ticket:
    try:
        ticket = Ticket.objects.get(id=ticket_id)
        return ticket
    except Ticket.DoesNotExist:
        raise TicketNotFoundException(f"Ticket {ticket_id} not found")


def update_ticket_count(ticket: Ticket, amount: int):
    ticket.count -= amount
    ticket.save()
