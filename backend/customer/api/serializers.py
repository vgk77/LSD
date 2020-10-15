from rest_framework import serializers

from ..models import Customer, Ticket


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = [
            'id',
            'name',
            'telegram_id'
        ]


class CustomerInTicketSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=256, required=True)
    telegram_id = serializers.IntegerField(required=True)

    def update(self, instance, validated_data):
        instance.name = validated_data['name']
        instance.telegram_id = validated_data['telegram_id']
        return instance


class TicketSerializer(serializers.ModelSerializer):
    customer = CustomerInTicketSerializer(required=True)
    number = serializers.IntegerField(read_only=True)
    attachments = serializers.FileField(required=False)

    class Meta:
        model = Ticket
        fields = [
            'number',
            'customer',
            'topic',
            'message',
            'status',
            'attachments',
        ]

    def create(self, validated_data):
        customer_data = validated_data.pop('customer')
        customer, created = Customer.objects.get_or_create(telegram_id=customer_data['telegram_id'])
        if created:
            customer.name = customer_data['name']
        return Ticket.objects.create(customer=customer, **validated_data)

    def update(self, instance, validated_data):
        if 'customer' in validated_data:
            customer_data = validated_data.pop('customer')
            instance.customer.name = customer_data['name']
            instance.customer.telegram_id = customer_data['telegram_id']
            instance.customer.save()

        if 'topic' in validated_data:
            instance.topic = validated_data['topic']
        if 'message' in validated_data:
            instance.message = validated_data['message']
        if 'status' in validated_data:
            instance.status = validated_data['status']
        if 'attachments' in validated_data:
            instance.attachments = validated_data['attachments']
        instance.save()
        return instance
