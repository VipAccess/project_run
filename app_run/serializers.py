from rest_framework import serializers
from .models import Run, AthleteInfo
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