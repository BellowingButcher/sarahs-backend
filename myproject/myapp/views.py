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
import math
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

        print(df.iloc[6, 2])
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
        df = pd.read_excel(obj[0]['schedule'], header=None)
        # df = df[df['TM Name'].str.contains('Kendra Sparks')]
        # print(df.iloc[7,2])
        # print(len(df.iloc[7,2]))
        a = df.iloc[49, 5]
        # print(a)
        b = a.split(':', 1)
        if len(b[0]) == 1:
            a = a[0:16]
            start = a[0:6]
            ending = a.split('-')
            ending = ending[1]

        elif len(b[0]) == 2:
            a = a[0:17]
            start = a[0:7]
            ending = a.split('-')
            ending = ending[1]

        else:
            print('data invalid :', b)

        # if len(ending) == 8:
        #     ending = ending[1:7]

        # elif len(ending) == 9:
        #     ending = ending[1:9]
        # print(len(ending))

        ending = ending.replace(' ', '')
        ending = ending.replace('(', '')
        # if ending.startswith(' '):
        #     ending = ending[1:LOE]
        # else:
        #     pass
        # if ending.endswith(' '):
        # LOE = len(ending)
        # if ending.endswith('('):
        #     ending = ending[0:LOE-1]
        # else: pass
        print('start time')
        print(start)
        print('end time')
        print(ending)

        if ending.endswith('AM') == True and ending.startswith('12') == True:
            ending = ending.replace('AM', '')
            ending = ending.replace('12', '00')
            # ending = ending.replace('PM', '')
            A = ending.split(':', 1)
            endHours = A[0]
            endMinutes = A[1]

        elif ending.endswith('PM') == True and ending.startswith('12') == True:
            ending = ending.replace('PM', '')
            A = ending.split(':', 1)
            endHours = A[0]
            endMinutes = A[1]

        elif ending.endswith('PM') == True and ending.startswith('12') == False:
            A = ending.split(':', 1)
            endHours = A[0]
            endHours = str(int(A[0])+12)
            endMinutes = A[1]
            endMinutes = endMinutes.replace('PM', '')
            # endMinutes = A[1]
            # endMinutes = endMinutes.replace('PM', '')

        elif ending.endswith('AM') == True and ending.startswith('12') == False:
            A = ending.split(':', 1)
            endHours = A[0]
            endMinutes = A[1].replace('AM', '')

        if start.endswith('AM') == True and start.startswith('12') == True:
            start = start.replace('AM', '')
            start = start.replace('12', '00')
            # start = start.replace('PM', '')
            A = start.split(':', 1)
            startHours = A[0]
            startMinutes = A[1]

        elif start.endswith('PM') == True and start.startswith('12') == True:
            start = start.replace('PM', '')
            A = start.split(':', 1)
            startHours = A[0]
            startMinutes = A[1]

        elif start.endswith('PM') == True and start.startswith('12') == False:
            A = start.split(':', 1)
            startHours = str(int(A[0])+12)
            startMinutes = A[1]
            startMinutes = startMinutes.replace('PM', '')

        elif start.endswith('AM') == True and start.startswith('12') == False:
            A = start.split(':', 1)
            startHours = A[0]
            startMinutes = A[1].replace('AM', '')

        # print('start hours')
        # print(startHours)
        # print('start minutes')
        # print(startMinutes)
        # print('end hours')
        # print(endHours)
        # print('end minutes')
        # print(endMinutes)

        startHourFloat = int(startHours) + (int(startMinutes)/(60))
        endHourFloat = int(endHours) + (int(endMinutes)/(60))
        print(startHourFloat)
        print(endHourFloat)
        totalHoursWorked = endHourFloat - startHourFloat
        print('total hours worked')
        print(totalHoursWorked)

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
