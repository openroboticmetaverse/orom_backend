from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from threading import Thread

from .models import Object, Robot, Scene
from .serializers import ObjectSerializer, RobotSerializer, SceneSerializer
from .utils import build_mujoco_image, run_mujoco_simulation_in_background



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
    """
    A viewset that controls the simulation container
    Currently only the POST-method is implemented
    """
    
    image_name = "sim_mujoco"                       # name of docker image
    dockerfile_path = "/app"                        # path to work directory inside the backend docker container
    dockerfile_name = "docker/Dockerfile_Mujoco"    # filepath of dockerfile
    container_port = 1345                           # port of simulation container #TODO: make dynamic
    host_port = 1345                                # port of frontend, constant because frontend container has only 1 websocket

    def post(self, request):
        # TODO: Check if container of that user and scene exists or is already running
        # TODO: How to generate unused port
        # TODO: Enable pulling from registry
        # TODO: Currently the config folder with robot models is copied into container -> get data from database
        # TODO: Check and improve logging of simulation container
        # TODO: Implement api to stop container
        try:
            # Build image if it does not exist
            build_mujoco_image(self.image_name, self.dockerfile_path, self.dockerfile_name)

            # Run the Mujoco simulation container asynchronously in a thread
            print("> Start simulation container")
            thread = Thread(target=run_mujoco_simulation_in_background,
                            args=(self.image_name, self.container_port, self.host_port, 
                                  request.data['user_id'], request.data['scene_id']))
            thread.start()

            # Respond with container information
            return Response({"message": "Simulation-Container starting", "host_port": self.host_port}, 
                            status=status.HTTP_201_CREATED)
        
        except Exception as ex:
            # Handle errors (e.g., container creation failure)
            print(str(ex))
            return Response({"error": str(ex)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
