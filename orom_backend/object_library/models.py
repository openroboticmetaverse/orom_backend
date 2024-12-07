from django.db import models
import os


class AbstractReference(models.Model):
    """Abstract class for common properties and functions"""
    name = models.CharField(max_length=255)
    file = models.CharField(max_length=255)
    file_type = models.CharField(max_length=255, editable=False)
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta: 
        abstract = True


class ReferenceObject(AbstractReference):
    """
    Database of objects the user can place in their scene.
    TODO: Make some objects only available for the user who uploaded it
    """


    def __str__(self):
        return f"ReferenceObject: {self.name} of type {self.file_type}"
    

    
class ReferenceRobot(AbstractReference):
    """
    Database of objects the user can place in their scene.
    TODO: Make some objects only available for the user who uploaded it
    """

    def __str__(self):
        return f"ReferenceRobot: {self.name} of type {self.file_type}"

