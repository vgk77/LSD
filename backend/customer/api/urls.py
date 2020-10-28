from django.urls import path

from rest_framework import routers

from .views import create_new_customer, TicketsViewSet

router = routers.DefaultRouter()
router.register(r'tickets', TicketsViewSet, 'tickets')

urlpatterns = [
    path('customers/', create_new_customer, name='create-new-customer'),
]

urlpatterns += router.urls
