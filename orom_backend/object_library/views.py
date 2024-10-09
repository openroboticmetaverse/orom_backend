from rest_framework import viewsets
from .models import ReferenceObject, ReferenceRobot
from .serializers import ReferenceObjectSerializer, ReferenceRobotSerializer
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your account has been created! You can now log in.')
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})


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