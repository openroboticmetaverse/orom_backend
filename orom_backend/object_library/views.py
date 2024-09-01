from rest_framework import generics
from .models import ReferenceObject, ReferenceRobot
from .serializers import ReferenceObjectSerializer, ReferenceRobotSerializer

# ReferenceObject Views
class ReferenceObjectListCreateView(generics.ListCreateAPIView):
    queryset = ReferenceObject.objects.all()
    serializer_class = ReferenceObjectSerializer

class ReferenceObjectDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ReferenceObject.objects.all()
    serializer_class = ReferenceObjectSerializer

# ReferenceRobot Views
class ReferenceRobotListCreateView(generics.ListCreateAPIView):
    queryset = ReferenceRobot.objects.all()
    serializer_class = ReferenceRobotSerializer

class ReferenceRobotDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ReferenceRobot.objects.all()
    serializer_class = ReferenceRobotSerializer