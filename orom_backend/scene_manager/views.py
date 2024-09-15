from rest_framework import viewsets
from .models import Object, Robot, Scene
from .serializers import ObjectSerializer, RobotSerializer, SceneSerializer


class ObjectViewSet(viewsets.ModelViewSet):
    """
    A viewset that provides the standard actions 
    (create, retrieve, update, partial_update, destroy, list)
    """
    queryset = Object.objects.all()
    serializer_class = ObjectSerializer


class RobotViewSet(viewsets.ModelViewSet):
    """
    A viewset that provides the standard actions 
    (create, retrieve, update, partial_update, destroy, list)
    """
    queryset = Robot.objects.all()
    serializer_class = RobotSerializer


class SceneViewSet(viewsets.ModelViewSet):
    """
    A viewset that provides the standard actions 
    (create, retrieve, update, partial_update, destroy, list)
    """
    queryset = Scene.objects.all()
    serializer_class = SceneSerializer
