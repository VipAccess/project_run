from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.conf import settings


@api_view(['GET'])
def get_company_details(request):
    """Get company public information."""
    data = {
        'company_name': settings.COMPANY_NAME,
        'slogan': settings.COMPANY_SLOGAN,
        'contacts': settings.COMPANY_CONTACTS
    }
    return Response(data)
