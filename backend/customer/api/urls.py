from django.contrib import admin
from django.urls import path, include

from .views import create_new_customer

urlpatterns = [
    path('customers/', create_new_customer, name='create-new-customer'),
]
