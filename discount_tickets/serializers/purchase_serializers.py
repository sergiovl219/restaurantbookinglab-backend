from rest_framework import serializers

from discount_tickets.models import Purchase


class PurchaseSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)

    class Meta:
        model = Purchase
        fields = [
            'id',
            'ticket',
            'guest',
            'quantity',
            'purchase_date'
        ]


class PurchaseTicketSerializer(serializers.Serializer):
    quantity = serializers.IntegerField()


class PurchaseTicketQueuedSerializer(serializers.Serializer):
    task_id = serializers.UUIDField()
