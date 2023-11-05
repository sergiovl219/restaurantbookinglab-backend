import uuid

from django.contrib.auth import get_user_model
from django.db import models
from discount_tickets.models.ticket import Ticket

User = get_user_model()


class Purchase(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    guest = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.PositiveIntegerField()
    purchase_date = models.DateTimeField(auto_now_add=True)
