from rest_framework import serializers
from .models import Scene, Object, Robot
from object_library.serializers import ReferenceRobotSerializer, ReferenceObjectSerializer


class SceneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Scene
        fields = '__all__'



class ObjectSerializer(serializers.ModelSerializer):
    # Nested serializer to also get information of reference object
#     object_reference = ReferenceObjectSerializer()
    object_reference = serializers.PrimaryKeyRelatedField(
        queryset=ReferenceObjectSerializer.Meta.model.objects.all(),
        write_only=True
    )
    object_reference_details = ReferenceObjectSerializer(source='object_reference', read_only=True)

    class Meta:
        model = Object
        fields = '__all__'



class RobotSerializer(serializers.ModelSerializer):
    # Nested serializer to also get information of reference robot
#     robot_reference = ReferenceRobotSerializer()
    robot_reference = serializers.PrimaryKeyRelatedField(
        queryset=ReferenceRobotSerializer.Meta.model.objects.all(),
        write_only=True
    )
    robot_reference_details = ReferenceRobotSerializer(source='robot_reference', read_only=True)

    class Meta:
        model = Robot
        fields = '__all__'
