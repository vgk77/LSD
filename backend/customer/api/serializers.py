from rest_framework import serializers

from ..models import Customer, Ticket


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = [
            'name',
            'telegram_id'
        ]
