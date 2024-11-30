from django.urls import path, include
from django.conf import settings
from .views import (
    ReferenceRobotViewSet, ReferenceObjectViewSet
)

# Use DefaultRouter if DEBUG is True, otherwise use SimpleRouter
if settings.DEBUG:
    from rest_framework.routers import DefaultRouter
    router = DefaultRouter()
else:
    from rest_framework.routers import SimpleRouter
    router = SimpleRouter()

router.register('ref-robots', ReferenceRobotViewSet)
router.register('ref-objects', ReferenceObjectViewSet)


urlpatterns = [
    path('', include(router.urls)),
]
