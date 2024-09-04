from django.urls import path, include
from .views import (
    ReferenceRobotViewSet, ReferenceObjectViewSet
)
from rest_framework.routers import SimpleRouter
router = SimpleRouter()
router.register('ref-robots', ReferenceRobotViewSet)
router.register('ref-objects', ReferenceObjectViewSet)


urlpatterns = [
    path('', include(router.urls)),
]
