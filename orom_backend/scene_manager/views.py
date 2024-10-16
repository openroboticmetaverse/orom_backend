from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Object, Robot, Scene
from .serializers import ObjectSerializer, RobotSerializer, SceneSerializer
from .utils import build_mujoco_image, run_mujoco_container



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



class MujocoSimulation(APIView):
    
    image_name = "sim_mujoco"
    dockerfile_path = "/app/docker/"
    dockefile_name = "Dockerfile_Mujoco"

    def post(self, request):
        # TODO: Check if container of that user and scene exists or is already running
        try:
            # Check if image exists or build it
            build_mujoco_image(self.image_name, self.dockerfile_path, self.dockefile_name)

            # Start a new MuJoCo simulation container
            print("> Execute run_mujoco_container")
            container = run_mujoco_container(self.image_name, request.data['user_id'], request.data['scene_id'])
            print(f"> Finished run_mujoco_container: ID {container.id}")

            # Respond with container information
            return Response({"container_id": container.id}, status=status.HTTP_201_CREATED)
        
        except Exception as ex:
            # Handle errors (e.g., container creation failure)
            print(str(ex))
            return Response({"error": str(ex)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
