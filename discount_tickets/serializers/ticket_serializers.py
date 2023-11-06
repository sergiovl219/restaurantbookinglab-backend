from rest_framework import serializers

from discount_tickets.models import Ticket


class TicketSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)

    class Meta:
        model = Ticket
        fields = [
            'id',
            'name',
            'count',
            'max_purchase',
        ]
