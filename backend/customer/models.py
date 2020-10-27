from django.db import models

from .enums import TypeOfTicketStatus


class Customer(models.Model):
    name = models.CharField(max_length=256)
    telegram_id = models.IntegerField(unique=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return F'[{self.telegram_id}] {self.name}'


class Ticket(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    customer = models.ForeignKey(
        'Customer',
        on_delete=models.SET_NULL,
        related_name='ticket',
        related_query_name='tickets',
        null=True,
        blank=True,
    )
    number = models.AutoField(primary_key=True)
    topic = models.TextField()
    message = models.TextField()
    attachments = models.FileField(blank=True, null=True)
    status = models.CharField(
        max_length=20,
        choices=TypeOfTicketStatus.CHOICES,
        default=TypeOfTicketStatus.new,
    )

    def __str__(self):
        return self.topic

    class Meta:
        ordering = ['-status']
