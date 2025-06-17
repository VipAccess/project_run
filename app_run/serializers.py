from rest_framework import serializers
from .models import Run, AthleteInfo, Challenge, Position, CollectibleItem
from django.contrib.auth.models import User


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
        fields = '__all__'

    def validate_latitude(self, value):
        if not (-90 <= float(value) <= 90):
            raise serializers.ValidationError(
                "Широта должна быть между -90 и 90")
        return value

    def validate_longitude(self, value):
        if not (-180 <= float(value) <= 180):
            raise serializers.ValidationError(
                "Долгота должна быть между -180 и 180")
        return value

    def validate_value(self, value):
        if value < 0:
            raise serializers.ValidationError(
                "Значение должно быть положительным")
        return value

