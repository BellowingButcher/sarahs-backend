from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from .models import Schedules
import pandas as pd
from django.db import IntegrityError
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        token = super(MyTokenObtainPairSerializer, cls).get_token(user)

        # Add custom claims

        token['username'] = user.username
        token['is_teamleader'] = user.is_teamleader
        token['is_teammember'] = user.is_teammember
        return token


class SchedulesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Schedules
        fields = '__all__'

class ScheduleParseAndSaveSerializer(SchedulesSerializer):
    beginning=serializers.DateTimeField(required=False)
    ending=serializers.DateTimeField(required=False)

class PatchScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Schedules
        fields = '__all__'
