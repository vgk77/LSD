from logging import getLogger

from django.db.models.signals import pre_save, pre_delete
from django.dispatch import receiver

from .models import Customer, Ticket


class Logger:
    @staticmethod
    @receiver(pre_save, sender=Customer)
    def save_customer(sender, instance, **kwargs):
        logger = getLogger(__name__)
        logger.info(msg=F'Customer is being saved. Name: {instance.name}, telegram_id: {instance.telegram_id}')

    @staticmethod
    @receiver(pre_save, sender=Ticket)
    def save_ticket(sender, instance, **kwargs):
        logger = getLogger(__name__)
        if instance.customer:
            telegram_id = instance.customer.telegram_id
        else:
            telegram_id = None
        logger.info(msg=F'Ticket is being saved. Number: {instance.number}, owner telegram_id: '
                        F'{telegram_id}, topic: {instance.topic}, message: {instance.message}, '
                        F'status: {instance.status}')

    @staticmethod
    @receiver(pre_delete, sender=Customer)
    def delete_customer(sender, instance, **kwargs):
        logger = getLogger(__name__)
        logger.info(msg=F'Customer is being deleted. Name: {instance.name}, telegram_id: {instance.telegram_id}')

    @staticmethod
    @receiver(pre_delete, sender=Ticket)
    def delete_ticket(sender, instance, **kwargs):
        logger = getLogger(__name__)
        if instance.customer:
            telegram_id = instance.customer.telegram_id
        else:
            telegram_id = None
        logger.info(msg=F'Ticket is being deleted. Number: {instance.number}, owner telegram_id: '
                        F'{telegram_id}, topic: {instance.topic}, message: {instance.message}, '
                        F'status: {instance.status}')
