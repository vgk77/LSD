from django.test import TestCase, Client

from ..models import Template


class TemplateApiTestCase(TestCase):
    def setUp(self) -> None:
        self.client = Client()

    def test_get_template(self):
        template = Template.objects.create(name='test_template', text='test template text')
        response = self.client.get(F'/api/templates/{template.name}/')
        self.assertContains(response, template.name, status_code=200)
        self.assertContains(response, template.text, status_code=200)

    def test_list_templates(self):
        template1 = Template.objects.create(name='test_template_1', text='first test template text')
        template2 = Template.objects.create(name='test_template_2', text='second test template text')
        response = self.client.get(F'/api/templates/')
        self.assertContains(response, template1.name, status_code=200)
        self.assertContains(response, template1.text, status_code=200)
        self.assertContains(response, template2.name, status_code=200)
        self.assertContains(response, template2.text, status_code=200)
