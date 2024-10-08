from rest_framework import generics
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