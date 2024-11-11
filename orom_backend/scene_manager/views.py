from threading import Thread
from queue import Queue
from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Object, Robot, Scene
from .serializers import ObjectSerializer, RobotSerializer, SceneSerializer
from .utils import build_mujoco_image, run_mujoco_simulation_in_background, stop_and_remove_container



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



class MujocoSimulationStart(APIView):
    """
    A viewset that starts the simulation container
    Currently only the POST-method is implemented
    """
    
    image_name = "sim_mujoco"                       # name of docker image
    dockerfile_path = "/app"                        # path to work directory inside the backend docker container
    dockerfile_name = "docker/Dockerfile_Mujoco"    # filepath of dockerfile
    container_port = 1345                           # port of simulation container #TODO: make dynamic
    host_port = 1345                                # port of frontend, constant because frontend container has only 1 websocket

    def post(self, request):
        # TODO: How to generate unused port
        # TODO: Check and improve logging of simulation container
        try:
            # Build image if it does not exist
            build_mujoco_image(self.image_name, self.dockerfile_path, self.dockerfile_name)

            print("> Start simulation container")

            # Queue for passing errors to api
            error_queue = Queue()

            # Run the Mujoco simulation container asynchronously in a thread
            thread = Thread(target=run_mujoco_simulation_in_background,
                            args=(self.image_name, self.container_port, self.host_port, 
                                  request.data['user_id'], request.data['scene_id'],
                                  error_queue
                                  )
                            )
            thread.start()

            # Wait for the thread to finish
            thread.join()

            # Check if any error was raised inside the thread
            if not error_queue.empty():
                error_message = error_queue.get()
                return error_message
            
            # Respond with container information
            return Response({"message": "Simulation-Container started"}, 
                            status=status.HTTP_200_OK)
        
        except Exception as ex:
            # Handle errors (e.g., container creation failure)
            print(str(ex))
            return Response({"message": str(ex)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class MujocoSimulationStop(APIView):
    """
    A viewset that stops and deleted a simulation container
    Currently only the POST-method is implemented
    """
    image_name = "sim_mujoco"

    def post(self, request):
        # Queue for passing errors to api
        error_queue = Queue()
        
        try:
            # Run in thread in case the stopping takes longer
            thread = Thread(target=stop_and_remove_container,
                            args=(
                                self.image_name, request.data['user_id'], request.data['scene_id'],
                                error_queue
                                )
                            )
            thread.start()
            # Wait for the thread to finish
            thread.join()

            # Check if any error was raised inside the thread
            if not error_queue.empty():
                error_message = error_queue.get()
                return error_message
            
            # Respond with container information
            return Response({"message": "Simulation-Container stopped and deleted"}, 
                            status=status.HTTP_200_OK)
        
        except Exception as ex:
            # Handle errors (e.g., container creation failure)
            print(str(ex))
            return Response({"message": str(ex)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    