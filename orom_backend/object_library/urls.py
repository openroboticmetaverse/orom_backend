from django.urls import path, include
from rest_framework.routers import SimpleRouter

from .views import (
    ReferenceRobotViewSet, ReferenceObjectViewSet
)



router = SimpleRouter()
router.register('ref-robots', ReferenceRobotViewSet)
router.register('ref-objects', ReferenceObjectViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
