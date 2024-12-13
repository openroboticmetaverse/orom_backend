from rest_framework import serializers
from .models import Scene, Object, Robot
from object_library.models import ReferenceRobot, ReferenceObject
from object_library.serializers import ReferenceRobotSerializer, ReferenceObjectSerializer


class SceneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Scene
        fields = '__all__'



class ObjectSerializer(serializers.ModelSerializer):
    class Meta:      
        model = Object
        fields = '__all__'



class RobotSerializer(serializers.ModelSerializer):
    robot_reference = serializers.PrimaryKeyRelatedField(queryset=ReferenceRobot.objects.all())

    class Meta:
        model = Robot
        fields = '__all__'
