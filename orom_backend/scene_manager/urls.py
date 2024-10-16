from django.urls import path, include
from .views import (
    ObjectViewSet, RobotViewSet, SceneViewSet, MujocoSimulation
)
from rest_framework.routers import SimpleRouter
router = SimpleRouter()
router.register('objects', ObjectViewSet)
router.register('robots', RobotViewSet)
router.register('scenes', SceneViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('run_simulation/', MujocoSimulation.as_view(), name='start_simulation'),
]
