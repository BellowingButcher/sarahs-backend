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

    # choice_set = QuestionChoiceSerializer(many=True) ????Unsure how this would fit????

    #Where does validated_data come from? 
    # def create(self, validated_data):
    #     from pprint import pprint
    #     pprint(validated_data)
    #     try:
    #         s = Schedules.objects.create(
    #             schedule= validated_data["blob_name"]["_location"]["path_"],
    #             uploaded_by= validated_data["schedule"],
    #             beginning= df.iloc[7,3],
    #             ending= df.iloc[7,8],
    #             status= "True",
    #         )      
    #         s.save()
    #         return s
    #     except IntegrityError as e:
    #         raise serializers.ValidationError({
    #             "errors":str(e)
    #         })
        # fields =({
            # 'schedule': self.data["blob_name"]["_location"]["path_"],
            # 'uploaded_by': self.data["schedule"],
            # 'beginning': df.iloc[7,3],
            # 'ending': df.iloc[7,8],
            # 'status': "True",
        # })
        # schedule_validated_data = validated_data.pop('choice_set')# unsure what I am supposed to do here. Im guessing its a type of array or list that contains the choice_set from line 28
        # question = Question.objects.create(**validated_data)# **validated data??
        # choice_set_serializer = self.fields['choice_set']
        # for each in choice_validated_data:
        #     each['question'] = question
        # choices = choice_set_serializer.create(choice_validated_data)
        # return schedule
