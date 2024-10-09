from django.urls import path, include
from object_manager import views 
#from django.contrib.auth import views as auth_views

from .views import (
    ReferenceRobotViewSet, ReferenceObjectViewSet
)
from rest_framework.routers import SimpleRouter
router = SimpleRouter()
router.register('ref-robots', ReferenceRobotViewSet)
router.register('ref-objects', ReferenceObjectViewSet)


urlpatterns = [
    path('', include(router.urls)),

    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout')
]
