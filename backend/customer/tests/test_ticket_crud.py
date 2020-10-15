from django.test import TestCase, Client

from ..models import Ticket, Customer


class TicketApiTestCase(TestCase):
    def setUp(self) -> None:
        self.client = Client()

    def test_create_ticket_without_attachments(self):
        ticket_data = {
            'customer': {
                'name': 'customer1',
                'telegram_id': 1
            },
            'topic': 'topic 1',
            'message': 'message 1',
            'status': 'New',
        }
        response = self.client.post('/api/tickets/', data=ticket_data, content_type='application/json')
        ticket, created = Ticket.objects.get_or_create(topic='topic 1')
        self.assertEqual(created, False)
        self.assertContains(response, ticket.customer.name, status_code=201)
        self.assertContains(response, ticket.customer.telegram_id, status_code=201)
        self.assertContains(response, ticket.topic, status_code=201)
        self.assertContains(response, ticket.message, status_code=201)
        self.assertContains(response, ticket.status, status_code=201)
        self.assertContains(response, ticket.number, status_code=201)

    def test_create_ticket_without_status(self):
        ticket_data = {
            'customer': {
                'name': 'customer1',
                'telegram_id': 1
            },
            'topic': 'topic 1',
            'message': 'message 1',
        }
        self.client.post('/api/tickets/', data=ticket_data, content_type='application/json')
        ticket, created = Ticket.objects.get_or_create(topic='topic 1')
        self.assertEqual(created, False)
        self.assertEqual(ticket.status, 'New')

    def test_get_ticket(self):
        ticket = Ticket.objects.create(topic='topic 2', message='message 2')
        response = self.client.get(F'/api/tickets/{ticket.number}/')
        self.assertContains(response, ticket.number, status_code=200)
        self.assertContains(response, ticket.topic, status_code=200)
        self.assertContains(response, ticket.message, status_code=200)
        self.assertContains(response, ticket.status, status_code=200)

    def test_delete_ticket(self):
        customer = Customer.objects.create(name='name1', telegram_id=121212)
        ticket = Ticket.objects.create(customer=customer, topic='topic 3', message='message 3')
        response = self.client.delete(F'/api/tickets/{ticket.number}/')
        self.assertContains(response, '', status_code=204)
        self.assertNotEqual(customer, None)
