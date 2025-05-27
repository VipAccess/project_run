from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import viewsets
from .serializers import RunSerializer, UserSerializer
from .models import Run
from django.contrib.auth.models import User
from project_run.settings import base
from rest_framework.filters import SearchFilter
from rest_framework.views import APIView
from rest_framework import status
from django.shortcuts import get_object_or_404


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
    filter_backends = [SearchFilter]
    search_fields = ['first_name', 'last_name']

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


class StartRunAPIView(APIView):
    def post(self, request, run_id):
        run = get_object_or_404(Run, id=run_id)
        if run.status != 'init':
            return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            run.status = 'in_progress'
            run.save()
            return Response({"status": "updated"})


class StopRunAPIView(APIView):
    def post(self, request, run_id):
        run = get_object_or_404(Run, id=run_id)
        if run.status == 'init':
            return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            run.status = 'finished'
            run.save()
            return Response({"status": "updated"})
