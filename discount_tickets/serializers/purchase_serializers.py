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


class PurchaseResponseSerializer(serializers.Serializer):
    id = serializers.UUIDField(read_only=True)
    ticket = serializers.UUIDField()
    guest = serializers.UUIDField(allow_null=True)
    quantity = serializers.IntegerField()
    purchase_date = serializers.DateTimeField()


class PurchaseTicketResultSerializer(serializers.Serializer):
    status = serializers.CharField()
    result = PurchaseResponseSerializer(required=False)
    error_message = serializers.CharField(required=False)


class PurchaseTicketSerializer(serializers.Serializer):
    quantity = serializers.IntegerField()


class PurchaseTicketQueuedSerializer(serializers.Serializer):
    task_id = serializers.UUIDField()
