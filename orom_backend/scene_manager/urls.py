from django.urls import path, include
from django.conf import settings
from .views import (
    ObjectViewSet, RobotViewSet, SceneViewSet, MujocoSimulationStart, MujocoSimulationStop
)


# Use DefaultRouter if DEBUG is True, otherwise use SimpleRouter
if settings.DEBUG:
    from rest_framework.routers import DefaultRouter
    router = DefaultRouter()
else:
    from rest_framework.routers import SimpleRouter
    router = SimpleRouter()

router.register('objects', ObjectViewSet)
router.register('robots', RobotViewSet)
router.register('scenes', SceneViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('run_simulation/', MujocoSimulationStart.as_view(), name='start_simulation'),
    path('stop_simulation/', MujocoSimulationStop.as_view(), name='stop_simulation'),
]
