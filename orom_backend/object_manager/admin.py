from django.contrib import admin
from .models import Scene, Object,Robot, GeometricObject

# Register your models here.
admin.site.register(Scene)
admin.site.register(Object)
admin.site.register(Robot)
admin.site.register(GeometricObject)