from django.urls import path
from .views import (
    ReferenceObjectListCreateView, 
    ReferenceObjectDetailView, 
    ReferenceRobotListCreateView, 
    ReferenceRobotDetailView
)

urlpatterns = [
    # ReferenceObject URLs
    path('ref-objects/', ReferenceObjectListCreateView.as_view(), name='reference-object-list-create'),
    path('ref-objects/<int:pk>/', ReferenceObjectDetailView.as_view(), name='reference-object-detail'),

    # ReferenceRobot URLs
    path('ref-robots/', ReferenceRobotListCreateView.as_view(), name='reference-robot-list-create'),
    path('ref-robots/<int:pk>/', ReferenceRobotDetailView.as_view(), name='reference-robot-detail'),
]
