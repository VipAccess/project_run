from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import viewsets
from .serializers import RunSerializer, UserSerializer, AthleteInfoSerializer
from .models import Run, AthleteInfo
from django.contrib.auth.models import User
from project_run.settings import base
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.views import APIView
from rest_framework import status
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination


@api_view(['GET'])
def company_details(request):
    return Response({
        'company_name': base.COMPANY_NAME,
        'slogan': base.SLOGAN,
        'contacts': base.CONTACTS
    })


class RunPagination(PageNumberPagination):
    page_size_query_param = 'size'


class RunViewSet(viewsets.ModelViewSet):
    queryset = Run.objects.select_related('athlete').all()
    serializer_class = RunSerializer
    pagination_class = RunPagination
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['status', 'athlete']
    ordering_fields = ['created_at']


class UserPagination(PageNumberPagination):
    page_size_query_param = 'size'


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = UserPagination
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['first_name', 'last_name']
    ordering_fields = ['date_joined']

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
        if run.status != 'in_progress':
            return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            run.status = 'finished'
            run.save()
            return Response({"status": "updated"})


class AthleteInfoAPIView(APIView):
    def get(self, request, user_id):
        user = get_object_or_404(User, id=user_id)
        weight = request.query_params.get('weight')
        goals = request.query_params.get('goals')
        if weight is None or 0 < int(weight) < 900:
            athlete_info, created = AthleteInfo.objects.get_or_create(
                user_id=user, weight=weight, goals=goals)
        else:
            return Response({'error': 'Invalid weight'},
                            status=status.HTTP_400_BAD_REQUEST)
        return Response({'user_id': user_id, 'weight': weight, 'goals': goals})

    def put(self, request, user_id):
        user = get_object_or_404(User, id=user_id)
        weight = request.query_params.get('weight')
        goals = request.query_params.get('goals')
        if weight is None or 0 < int(weight) < 900:
            athlete, created = AthleteInfo.objects.update_or_create(
                user_id=user,
                defaults={
                    'weight': weight,
                    'goals': goals,
                }
            )
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response({
            "user_id": user_id,
            "weight": weight,
            "goals": goals,
        }, status=status.HTTP_201_CREATED)
