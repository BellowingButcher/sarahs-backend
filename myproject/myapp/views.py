from django.shortcuts import render
from rest_framework.views import APIView
# djsr/authentication/views.py
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import permissions, generics
from .serializers import MyTokenObtainPairSerializer, SchedulesSerializer
from .models import Schedules


class ObtainTokenPairWithColorView(TokenObtainPairView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = MyTokenObtainPairSerializer


class SaveSchedule(generics.ListCreateAPIView):
    queryset = Schedules.objects.all()
    serializer_class = SchedulesSerializer
    permissions_classes = (permissions.AllowAny,)
