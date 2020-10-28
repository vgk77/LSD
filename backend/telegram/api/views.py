from rest_framework.decorators import api_view
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema

from customer.api.serializers import TicketSerializer
from customer.models import Ticket
from ..models import Template
from .serializers import TemplateSerializer


@swagger_auto_schema(methods=['GET'], responses={'200': TicketSerializer})
@api_view(['GET'])
def get_tickets_by_telegram_id(request, telegram_id):
    if request.method == 'GET':
        serializer = TicketSerializer(Ticket.objects.filter(customer__telegram_id=telegram_id), many=True)
        return Response(serializer.data, status=200)


class TemplateViewSet(GenericViewSet, ListModelMixin, RetrieveModelMixin):
    queryset = Template.objects.all()
    serializer_class = TemplateSerializer
    lookup_field = 'name'
