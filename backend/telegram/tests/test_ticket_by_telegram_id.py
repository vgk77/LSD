from django.test import TestCase, Client

from ..models import Template
from customer.models import Ticket, Customer


class TicketByTelegramIdApiTestCase(TestCase):
    def setUp(self) -> None:
        self.client = Client()

    def test_get_ticket(self):
        customer = Customer.objects.create(name='test_customer', telegram_id='202020')
        ticket = Ticket.objects.create(customer=customer, topic='test topic', message='test message')
        response = self.client.get(F'/api/tickets/by-user-id/{customer.telegram_id}')
        self.assertContains(response, ticket.topic, status_code=200)
        self.assertContains(response, ticket.message, status_code=200)
