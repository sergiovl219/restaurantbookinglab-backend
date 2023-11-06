from discount_tickets.models import Ticket
from restaurant.models import Restaurant


def get_tickets_for_restaurant(restaurant: Restaurant):
    tickets = Ticket.objects.filter(restaurant=restaurant)
    return tickets


def get_ticket_for_restaurant(ticket_id, restaurant: Restaurant):
    try:
        ticket = Ticket.objects.get(id=ticket_id, restaurant=restaurant)
        return ticket
    except Ticket.DoesNotExist:
        return None
