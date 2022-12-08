from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
# djsr/authentication/views.py
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import permissions, generics
from .serializers import MyTokenObtainPairSerializer, SchedulesSerializer, ScheduleParseAndSaveSerializer
from .models import Schedules
from .firebase import storage
import numpy as np
import pandas as pd
from django.utils.timezone import make_aware
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

        # print(df.iloc[6,3])
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
        # df = pd.read_excel(request.data["schedule"], header=None)
        # print(df.iloc[7,8])
        # for index, row in contents.iterrows():
        #     print(index, row)
    #     # source_blob_name = request.data["blob_name"]["_location"]["path_"]
    #     # destination_file_name = request.data["schedule"]
    #     # blob = storage.bucket.blob(source_blob_name)
    #     # data = blob.download(destination_file_name)
    #     # print(data)
        # schedule = Schedules({
        #     'schedule': request.data["blob_name"]["_location"]["path_"],
        #     'uploaded_by': request.data["schedule"],
        #     'beginning': df.iloc[7,3],
        #     'ending': df.iloc[7,8],
        #     'status': "True",
        # })
        # schedule.objects.create()

        return Response('Maybe')


# def hello_world(request):
#     if request.method == 'POST':
#         return Response({"message": "Got some data!", "data": request.data})
#     return Response({"message": "Hello, world!"})
