import uuid

from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.signals import post_save
from django.db.models.signals import pre_save
from django.dispatch import receiver

from discount_tickets.helpers import ticket_helper
from discount_tickets.models.ticket import Ticket

User = get_user_model()


class Purchase(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    guest = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.PositiveIntegerField()
    purchase_date = models.DateTimeField(auto_now_add=True)


@receiver(pre_save, sender=Purchase)
def handle_purchase_pre_save(sender, instance, **kwargs):
    ticket = instance.ticket
    quantity = instance.quantity
    max_purchase = ticket.max_purchase

    if ticket.count <= 0:
        # TODO: Custom exception
        raise Exception
    if quantity > max_purchase:
        # TODO: Custom exception
        raise Exception


@receiver(post_save, sender=Purchase)
def handle_purchase_post_save(sender, instance, created, **kwargs):
    if created:
        ticket = instance.ticket
        quantity = instance.quantity
        ticket_helper.update_ticket_count(ticket, quantity)
