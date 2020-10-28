from django.urls import path

from rest_framework import routers

from .views import get_tickets_by_telegram_id, TemplateViewSet

router = routers.DefaultRouter()
router.register(r'templates', TemplateViewSet, 'templates')

urlpatterns = [
    path('tickets/by-user-id/<int:telegram_id>', get_tickets_by_telegram_id, name='get-tickets-by-telegram-id')
]

urlpatterns += router.urls
