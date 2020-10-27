from django.contrib import admin
from django.urls import path

from rest_framework import routers

from .views import create_new_customer, get_tickets_by_telegram_id, TicketsViewSet

router = routers.DefaultRouter()
router.register(r'tickets', TicketsViewSet, 'tickets')

urlpatterns = [
    path('customers/', create_new_customer, name='create-new-customer'),
    path('tickets/by-user-id/<int:telegram_id>', get_tickets_by_telegram_id, name='get-tickets-by-telegram-id')
]

urlpatterns += router.urls
