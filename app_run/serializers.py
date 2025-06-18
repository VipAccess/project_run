from rest_framework import serializers
from .models import Run, AthleteInfo, Challenge, Position, CollectibleItem
from django.contrib.auth.models import User
from django.core.validators import URLValidator


class UserForRunSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'last_name', 'first_name']


class RunSerializer(serializers.ModelSerializer):
    athlete_data = UserForRunSerializer(source='athlete', read_only=True)

    class Meta:
        model = Run
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    type = serializers.SerializerMethodField()
    runs_finished = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'date_joined', 'username', 'last_name', 'first_name',
                  'type', 'runs_finished']

    def get_type(self, obj):
        if not obj.is_superuser:
            if obj.is_staff:
                return "coach"
            else:
                return "athlete"
        return None

    def get_runs_finished(self, obj):
        return obj.run_set.filter(status='finished').count()


class AthleteInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = AthleteInfo
        fields = '__all__'


class ChallengeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Challenge
        fields = '__all__'


class PositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Position
        fields = ['id', 'run', 'latitude', 'longitude']

    def validate(self, data):
        if data['run'].status != 'in_progress':
            raise serializers.ValidationError(
                "Забег должен быть в статусе 'in_progress' для добавления позиций"
            )
        if not (-90.0 < data['latitude'] < 90.0):
            raise serializers.ValidationError(
                "Широта должна находиться в диапазоне от -90.0 до +90.0 градусов."
            )
        if not (-180.0 < data['longitude'] < 180.0):
            raise serializers.ValidationError(
                "Долгота должна находиться в диапазоне от -180.0 до +180.0 градусов."
            )

        return data


class CollectibleItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CollectibleItem
        fields = ['name', 'uid', 'latitude', 'longitude', 'picture', 'value']

    def validate_latitude(self, value):
        if value > 90 or value < -90:
            raise serializers.ValidationError('latitude должен быть в диапазоне от -90.0 до +90.0 градусов')
        return value

    def validate_longitude(self, value):
        if value > 180 or value < -180:
            raise serializers.ValidationError('longitude должен быть в диапазоне от -180.0 до +180.0 градусов')
        return value
