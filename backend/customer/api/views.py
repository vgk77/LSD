from rest_framework.decorators import api_view
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema

from .serializers import CustomerSerializer, TicketSerializer
from ..models import Ticket


@swagger_auto_schema(methods=['POST'], request_body=CustomerSerializer)
@api_view(['POST'])
def create_new_customer(request):
    if request.method == 'POST':
        serializer = CustomerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class TicketsViewSet(ModelViewSet):
    def get_queryset(self):
        return Ticket.objects.all()
    serializer_class = TicketSerializer


@api_view(['GET'])
def get_tickets_by_telegram_id(request, telegram_id):
    if request.method == 'GET':
        serializer = TicketSerializer(Ticket.objects.filter(customer__telegram_id=telegram_id), many=True)
        return Response(serializer.data, status=200)
