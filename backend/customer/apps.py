from django.apps import AppConfig


class CustomerAppConfig(AppConfig):
    name = 'customer'

    def ready(self):
        from .logging import Logger
        Logger()
