from rest_framework import serializers
from .models import Scene, Object, Robot
# TODO: Check out for Scene: https://github.com/MattBroach/DjangoRestMultipleModels

class SceneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Scene
        fields = '__all__'


class ObjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Object
        fields = '__all__'


class RobotSerializer(serializers.ModelSerializer):
    class Meta:
        model = Robot
        fields = '__all__'
