from django.urls import path, include
from .views import (
    ObjectViewSet, RobotViewSet, SceneViewSet
)
from rest_framework.routers import SimpleRouter
router = SimpleRouter()
router.register('objects', ObjectViewSet)
router.register('robots', RobotViewSet)
router.register('scenes', SceneViewSet)


urlpatterns = [
    path('', include(router.urls)),
]
