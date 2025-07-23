from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import viewsets
from django.conf import settings

from app_run.models import (
    Run
)
from app_run.serializers import (
    RunSerializer
)


@api_view(['GET'])
def get_company_details(request):
    """Get company public information."""
    data = {
        'company_name': settings.COMPANY_NAME,
        'slogan': settings.COMPANY_SLOGAN,
        'contacts': settings.COMPANY_CONTACTS
    }
    return Response(data)


class RunViewSet(viewsets.ModelViewSet):
    queryset = Run.objects.all()
    serializer_class = RunSerializer
