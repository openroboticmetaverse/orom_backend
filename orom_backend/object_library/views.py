from rest_framework import viewsets
from .models import ReferenceObject, ReferenceRobot
from .serializers import ReferenceObjectSerializer, ReferenceRobotSerializer



class ReferenceRobotViewSet(viewsets.ModelViewSet):
    """
    A viewset that provides the standard actions 
    (create, retrieve, update, partial_update, destroy, list)
    """
    queryset = ReferenceRobot.objects.all()
    serializer_class = ReferenceRobotSerializer



class ReferenceObjectViewSet(viewsets.ModelViewSet):
    """
    A viewset that provides the standard actions 
    (create, retrieve, update, partial_update, destroy, list)
    """
    queryset = ReferenceObject.objects.all()
    serializer_class = ReferenceObjectSerializer