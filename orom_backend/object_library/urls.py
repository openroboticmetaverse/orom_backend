from django.urls import path
from object_manager import views 
from django.contrib.auth import views as auth_views

 # Import views from object_manager
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

    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]
