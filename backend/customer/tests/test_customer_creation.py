from django.test import TestCase, Client

from ..models import Customer


class CustomerApiTestCase(TestCase):
    def setUp(self) -> None:
        self.client = Client()

    def test_create_customer_full_data(self):
        customer_data = {
            'name': 'customer1',
            'telegram_id': 12345,
        }
        response = self.client.post('/api/customers/', data=customer_data, content_type='application/json')
        customer, created = Customer.objects.get_or_create(telegram_id=12345)
        self.assertEqual(created, False)
        self.assertContains(response, customer.telegram_id, status_code=201)
        self.assertContains(response, customer.name, status_code=201)

    def test_create_customer_without_parameters(self):
        customer_data = {
            'name': 'customer2'
        }
        response = self.client.post('/api/customers/', data=customer_data, content_type='application/json')
        self.assertContains(response, 'This field is required', status_code=400)
