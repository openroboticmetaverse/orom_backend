from django.db import models
from django.contrib.postgres.fields import ArrayField

from object_library.models import ReferenceObject, ReferenceRobot


class Scene(models.Model):
    """
    Projects created by users are defined as a scene
    """
    name = models.CharField(max_length=255)
    # TODO: Add connections to user ones they exist
    # user_id = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Scene: {self.name}"



class AbstractObject(models.Model):
    """Abstract class for common properties and functions"""
    name = models.CharField(max_length=255)
    scene_id = models.ForeignKey(Scene, on_delete=models.CASCADE)   # if a scene is deleted, all connected objects are deleted
    position = ArrayField(models.FloatField(), size=3, null=True, blank=True)              # [x, y, z]
    orientation = ArrayField(models.FloatField(), size=3, null=True, blank=True)           # [roll, pitch, yaw]
    scale = ArrayField(models.FloatField(), size=3, null=True, blank=True)                 # [x, y, z]
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta: 
        abstract = True



class Robot(AbstractObject):
    """
    Inherits all properties from the Object-class and extends them with robot specific information
    """
    robot_reference = models.ForeignKey(ReferenceRobot, on_delete=models.CASCADE)
    joint_angles = ArrayField(models.FloatField(), null=True, blank=True)

    def __str__(self):
        return f"Robot: {self.name} ({self.robot_reference.name}) of Scene {self.scene_id.name}"
    
    def save(self, *args, **kwargs):
        if not self.position: self.position = [0.0, 0.0, 0.0]
        if not self.orientation: self.orientation = [0.0, 0.0, 0.0]
        if not self.scale: self.scale = [1.0, 1.0, 1.0]
        if not self.joint_angles: self.joint_angles = [0.0] * self.robot_reference.num_joints
        super().save(*args, **kwargs)



class Object(AbstractObject):
    """
    Inherits all properties from the AbstractObject-class and extends them with object specific information
    """
    object_reference = models.ForeignKey(ReferenceObject, on_delete=models.CASCADE)
    color = models.CharField(max_length=7, null=True, blank=True)

    def __str__(self):
        return f"Object: {self.name} of Scene {self.scene_id.name}"
    
    def save(self, *args, **kwargs):
        if not self.position: self.position = [0.0, 0.0, 0.0]
        if not self.orientation: self.orientation = [0.0, 0.0, 0.0]
        if not self.scale: self.scale = [1.0, 1.0, 1.0]
        super().save(*args, **kwargs)
