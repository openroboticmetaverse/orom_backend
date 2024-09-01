from django.db import models


class ReferenceObject(models.Model):
    """
    Database of objects the user can place in their scene.
    TODO: Make some objects only available for the user who uploaded it
    """
    name = models.CharField(max_length=255)
    file = models.FileField(upload_to='object_files/')
    file_type = models.CharField(max_length=255, editable=False) # TODO: set automatically on change
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"ReferenceObject: {self.name} of type {self.file_type}"



class ReferenceRobot(ReferenceObject):
    """
    Database of objects the user can place in their scene.
    TODO: Make some objects only available for the user who uploaded it
    """
    num_joints = models.IntegerField()

    def __str__(self):
        return f"ReferenceRobot: {self.name} of type {self.file_type}"

