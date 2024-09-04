from rest_framework import serializers
from .models import ReferenceObject, ReferenceRobot

class ReferenceObjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReferenceObject
        #exclude = ('file_type')
        fields = '__all__'



class ReferenceRobotSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReferenceRobot
        fields = '__all__'

# TODO: Check out for Scene: https://github.com/MattBroach/DjangoRestMultipleModels