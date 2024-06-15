# While testing my project, this file is used to reset my PK of the video db

from django.core.management.base import BaseCommand
from django.db import connection
from video.models import Video  # Replace with your actual model

class Command(BaseCommand):
    help = 'Clears data and resets primary key sequence'

    def handle(self, *args, **kwargs):
        # Delete all data from the model
        Video.objects.all().delete()
        self.stdout.write(self.style.SUCCESS('Deleted all data from MyModel'))

        # Reset primary key sequence for SQLite
        with connection.cursor() as cursor:
            cursor.execute(f"DELETE FROM sqlite_sequence WHERE name='{Video._meta.db_table}';")
        self.stdout.write(self.style.SUCCESS('Reset primary key sequence for MyModel'))


