from django.db import models
from django.contrib.postgres.fields import ArrayField

from object_library.models import ReferenceObject, ReferenceRobot
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models

class CustomUserManager(BaseUserManager):
    def create_user(self, email, username, password=None):
        if not email:
            raise ValueError('Users must have an email address')
        if not username:
            raise ValueError('Users must have a username')

        user = self.model(
            email=self.normalize_email(email),
            username=username,
        )
        user.set_password(password)  # Hash the password
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None):
        user = self.create_user(email, username, password)
        user.is_admin = True
        user.save(using=self._db)
        return user

class CustomUser(AbstractBaseUser):
    email = models.EmailField(max_length=255, unique=True)
    username = models.CharField(max_length=255, unique=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'  # Use email to log in
    REQUIRED_FIELDS = ['username']  # Username is required in addition to email

    def __str__(self):
        return self.email


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

    def create(self):
        pass  # Implement the logic for creating a Scene

    def delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)



class Object(models.Model):
    """
    Storing properties of placed objects
    """
    name = models.CharField(max_length=255)
    scene_id = models.ForeignKey(Scene, on_delete=models.CASCADE)   # if a scene is deleted, all connected objects are deleted
    object_reference = models.ForeignKey(ReferenceObject, on_delete=models.CASCADE) # if reference object is deleted, all objects used in scenes are deleted
    position = ArrayField(models.FloatField(), size=3, null=True, blank=True)              # [x, y, z]
    orientation = ArrayField(models.FloatField(), size=3, null=True, blank=True)           # [roll, pitch, yaw]
    scale = ArrayField(models.FloatField(), size=3, null=True, blank=True)                 # [x, y, z]
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Object: {self.name} of Scene {self.scene_id.name}"

    def create(self):
        pass  # Implement the logic for creating an Object

    def delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)

    def move(self, x, y, z, roll, pitch, yaw):
        pass  # Implement the logic for moving the Object



class Robot(Object):
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
        print(self.joint_angles)
        super().save(*args, **kwargs)

    def move(self, x, y, z, roll, pitch, yaw):
        pass  # Implement the logic for moving the Robot



class GeometricObject(Object):
    """
    Inherits all properties from the Object-class and extends them with geometric object information
    -> not sure yet if this is the right way, maybe just use the Object-class itself
    """
    color = models.CharField(max_length=7)  # RGB Code in the form of a string

    def __str__(self):
        return f"GeometricObject: {self.name} of Scene {self.scene_id.name}"