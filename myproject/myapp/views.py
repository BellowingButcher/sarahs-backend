from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
# djsr/authentication/views.py
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import permissions, generics
from .serializers import MyTokenObtainPairSerializer, SchedulesSerializer, ScheduleParseAndSaveSerializer, PatchScheduleSerializer
from .models import Schedules
from .firebase import storage
import numpy as np
import pandas as pd
from django.utils.timezone import make_aware
import json
# import glob
# from .firebase import firebase


class ObtainTokenPairWithColorView(TokenObtainPairView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = MyTokenObtainPairSerializer


class SaveSchedule(generics.ListCreateAPIView):
    queryset = Schedules.objects.all()
    serializer_class = SchedulesSerializer

    def create(self, request):

        df = pd.read_excel(request.data["schedule"], header=None)

        print(df.iloc[6,2])
        data = {
            'schedule': request.data["schedule"],
            'uploaded_by': request.user.id,
            'beginning': df.iloc[6, 3],
            'ending': df.iloc[6, 9],
            'status': "True",
        }
        serializer = SchedulesSerializer(data=data)
        if serializer.is_valid():
            naive_beginning = df.iloc[6, 3]
            naive_ending = df.iloc[6, 8]
            aware_beginning = make_aware(naive_beginning)
            aware_ending = make_aware(naive_ending)
            try:
                obj = Schedules.objects.get(
                    beginning=aware_beginning, ending=aware_ending,)
                return Response(
                    "Schedule already exists"
                )
            except Schedules.DoesNotExist:
                serializer.save()

            return Response({
                "data": serializer.data
            })
        else:
            return Response({
                "errors": serializer.errors
            })
        return Response('Maybe')

class PatchSchedule(generics.RetrieveUpdateDestroyAPIView):
    queryset = Schedules.objects.all()
    serializer_class = PatchScheduleSerializer

class TeamMemberGraph(generics.ListCreateAPIView):
    queryset = Schedules.objects.all()
    serializer_class = SchedulesSerializer
    def list(self, request):
        queryset = self.get_queryset()
        serializer = SchedulesSerializer(queryset, many=True)
        data = []
        obj = json.loads(json.dumps(serializer.data))
        df= pd.read_excel(obj[0]['schedule'], header=None)
        a = df.iloc[16,3]
        print(a)
        # for x in obj:
        #     df = pd.read_excel(x['schedule'], header=None)

        #     data.append(x['schedule'])
        # print(data)
        # for i in obj:
        #     print(i.schedule)
        # print(getattr(obj,'schedule'))
        # print(obj[0]['schedule'])
        # print (hasattr(obj,'schedule'))

        return Response(serializer.data)