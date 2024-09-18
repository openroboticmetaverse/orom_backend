from rest_framework import serializers
from .models import Scene, Object, Robot
from object_library.serializers import ReferenceRobotSerializer, ReferenceObjectSerializer


class SceneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Scene
        fields = '__all__'



class ObjectSerializer(serializers.ModelSerializer):
    # Nested serializer to also get information of reference object
    object_reference = ReferenceObjectSerializer()

    class Meta:
        model = Object
        fields = '__all__'



class RobotSerializer(serializers.ModelSerializer):
    # Nested serializer to also get information of reference robot
    robot_reference = ReferenceRobotSerializer()

    class Meta:
        model = Robot
        fields = '__all__'
