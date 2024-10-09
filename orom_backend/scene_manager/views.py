from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
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

    def retrieve(self, request, *args, **kwargs):
        """
        Overwrite retrieve function to also get information of objects and robots to visualize the scene for the user
        """
        scene = self.get_object()

        # Fetch all Robots and Objects that belong to this Scene
        robots = Robot.objects.filter(scene_id=scene)
        objects = Object.objects.filter(scene_id=scene)

        # Serialize the data
        scene_serializer = SceneSerializer(scene)
        robot_serializer = RobotSerializer(robots, many=True)
        object_serializer = ObjectSerializer(objects, many=True)

        # Return combined data
        return Response({
            'scene': scene_serializer.data,
            'robots': robot_serializer.data,
            'objects': object_serializer.data
        }, status=status.HTTP_200_OK)
