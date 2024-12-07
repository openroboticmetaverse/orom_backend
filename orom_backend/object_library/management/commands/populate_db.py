import requests
from django.conf import settings
from django.core.management.base import BaseCommand
from object_library.models import ReferenceObject, ReferenceRobot

class Command(BaseCommand):
    help = 'Populate the database with data from the model library hosted on GitHub'

    def handle(self, *args, **kwargs):
        """
        Main method to handle the command execution.
        Fetches data from the model library and populates the database.
        """
        # Fetch the reference library data from the specified URL
        response = requests.get(settings.MODEL_LIBRARY_URL)
        response.raise_for_status()  # Raise an error for bad status codes
        data = response.json()

        # Prefix URL for accessing the raw files from the GitHub repository
        prefix = "https://api.github.com/repos/openroboticmetaverse/robot-description/contents/"

        # Populate robots in the database
        for robot in data['robots']:
            ReferenceRobot.objects.update_or_create(
                name=robot['name'],
                defaults={
                    'file': prefix + robot['file'],
                    'file_type': robot['file_type'],
                    'description': robot['description'],
                    'created_at': robot['created_at'],
                    'updated_at': robot['updated_at'],
                }
            )

        # Populate objects in the database
        for obj in data['objects']:
            ReferenceObject.objects.update_or_create(
                name=obj['name'],
                defaults={
                    'file': prefix + obj['file'],
                    'file_type': obj['file_type'],
                    'description': obj['description'],
                    'created_at': obj['created_at'],
                    'updated_at': obj['updated_at'],
                }
            )

        self.stdout.write(self.style.SUCCESS('Successfully populated the database'))