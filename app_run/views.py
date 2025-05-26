from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import viewsets
from .serializers import RunSerializer, UserSerializer
from .models import Run
from django.contrib.auth.models import User
from project_run.settings import base


@api_view(['GET'])
def company_details(request):
    return Response({
        'company_name': base.COMPANY_NAME,
        'slogan': base.SLOGAN,
        'contacts': base.CONTACTS
    })


class RunViewSet(viewsets.ModelViewSet):
    queryset = Run.objects.select_related('athlete').all()
    serializer_class = RunSerializer


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_queryset(self):
        qs = self.queryset
        type_user = self.request.query_params.get('type', None)
        if type_user == 'coach':
            qs = qs.filter(is_staff=True, is_superuser=False)
        elif type_user == 'athlete':
            qs = qs.filter(is_staff=False, is_superuser=False)
        else:
            qs = qs.filter(is_superuser=False)
        return qs
