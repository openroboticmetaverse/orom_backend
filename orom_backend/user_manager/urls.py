from django.urls import path, include
from .views import register, login_view, logout_view
#from django.contrib.auth import views as auth_views



urlpatterns = [
    path('register/', register, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
]
