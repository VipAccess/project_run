from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import viewsets
from urllib3 import request

from rest_framework.parsers import MultiPartParser
from openpyxl import load_workbook
from .serializers import RunSerializer, UserSerializer, AthleteInfoSerializer
from .serializers import ChallengeSerializer, PositionSerializer, \
    CollectibleItemSerializer
from .models import Run, AthleteInfo, Challenge, Position, CollectibleItem
from django.contrib.auth.models import User
from project_run.settings import base
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.views import APIView
from rest_framework import status
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination
from geopy.distance import geodesic
from django.db.models import Sum
import io

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
            positions = run.position_set.all()

            total_distance = 0.0
            prev_point = None

            for position in positions:
                current_point = (position.latitude, position.longitude)
                if prev_point:
                    total_distance += geodesic(prev_point,
                                               current_point).kilometers
                prev_point = current_point

            run.distance = total_distance
            run.status = 'finished'
            run.save()

            finished_runs = Run.objects.filter(athlete=run.athlete,
                                               status='finished').count()
            if finished_runs == 10:
                Challenge.objects.get_or_create(
                    athlete=run.athlete,
                    defaults={
                        'full_name': 'Сделай 10 Забегов!'
                    }
                )

            total_distance_sum = Run.objects.filter(
                athlete=run.athlete,
                status='finished'
            ).aggregate(Sum('distance'))['distance__sum'] or 0

            if total_distance_sum >= 50:
                Challenge.objects.get_or_create(
                    athlete=run.athlete,
                    defaults={
                        'full_name': 'Пробеги 50 километров!'
                    }
                )

            return Response({"status": "updated"})


class AthleteInfoAPIView(APIView):
    def get(self, request, user_id):
        user = get_object_or_404(User, id=user_id)
        athlete_info, created = AthleteInfo.objects.get_or_create(user_id=user)
        serializer = AthleteInfoSerializer(athlete_info)
        return Response(serializer.data)

    def put(self, request, user_id):
        user = get_object_or_404(User, id=user_id)
        weight = request.data.get('weight')
        goals = request.data.get('goals')
        if weight is None or (weight.isdigit() and 0 < int(weight) < 900):
            athlete_info, created = AthleteInfo.objects.update_or_create(
                user_id=user,
                defaults={
                    'weight': weight,
                    'goals': goals,
                }
            )
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        serializer = AthleteInfoSerializer(athlete_info)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ChallengeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Challenge.objects.all()
    serializer_class = ChallengeSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['athlete']


class PositionViewSet(viewsets.ModelViewSet):
    queryset = Position.objects.all()
    serializer_class = PositionSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['run']


class CollectibleItemViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = CollectibleItem.objects.all()
    serializer_class = CollectibleItemSerializer


class UploadFileAPIView(APIView):
    parser_classes = [MultiPartParser]

    def post(self, request):
        if 'file' not in request.FILES:
            return Response({"error": "No file uploaded"}, status=status.HTTP_400_BAD_REQUEST)

        file = request.FILES['file']
        if not file.name.endswith('.xlsx'):
            return Response({"error": "File must be in XLSX format"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            wb = load_workbook(filename=io.BytesIO(file.read()))
            sheet = wb.active
            invalid_rows = []
            created_count = 0

            for row in sheet.iter_rows(min_row=2, values_only=True):  # пропускаем заголовок
                try:
                    # Валидация данных
                    if len(row) != 6:
                        invalid_rows.append(list(row))
                        continue

                    name, uid, lat, lon, picture, value = row

                    # Проверка типов данных
                    if not isinstance(name, str) or not isinstance(uid, str) or not isinstance(picture, str):
                        invalid_rows.append(list(row))
                        continue

                    try:
                        lat = float(lat)
                        lon = float(lon)
                        value = int(value)
                    except (ValueError, TypeError):
                        invalid_rows.append(list(row))
                        continue

                    # Проверка диапазонов
                    if not (-90 <= lat <= 90) or not (-180 <= lon <= 180):
                        invalid_rows.append(list(row))
                        continue

                    # Создание объекта
                    CollectibleItem.objects.create(
                        name=name,
                        uid=uid,
                        latitude=lat,
                        longitude=lon,
                        picture=picture,
                        value=value
                    )
                    created_count += 1

                except Exception as e:
                    invalid_rows.append(list(row))

            return Response({
                "created": created_count,
                "invalid_rows": invalid_rows
            }, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)