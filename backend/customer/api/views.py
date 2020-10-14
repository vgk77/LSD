from rest_framework.decorators import api_view
from rest_framework.response import Response

from .serializers import CustomerSerializer


@api_view(['POST'])
def create_new_customer(request):
    if request.method == 'POST':
        serializer = CustomerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

