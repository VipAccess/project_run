from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import viewsets
from .serializers import RunSerializer
from .models import Run


@api_view(['GET'])
def company_details(request):
    return Response({
        'company_name': 'Красные кеды',
        'slogan': 'Одна нога здесь, другая там!',
        'contacts': 'Город Красноярск, улица 30 Лет СССР, дом 30'
    })


class RunViewSet(viewsets.ModelViewSet):
    queryset = Run.objects.all()
    serializer_class = RunSerializer
