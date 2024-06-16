# While testing my project, this file is used to reset my PK of the video db

from django.core.management.base import BaseCommand
from django.db import connection
from video.models import Video  # Replace with your actual model

import os
from django.core.management.base import BaseCommand
from django.conf import settings
from video.models import Video

class Command(BaseCommand):
    help = 'Deletes all video files on disk and clears data'

    def handle(self, *args, **kwargs):
        # Delete all video files on disk
        videos = Video.objects.all()

        for video in videos:
            try:
                file_path = os.path.join(settings.MEDIA_ROOT, str(video.video_file))
                if os.path.exists(file_path):
                    os.remove(file_path)
                    self.stdout.write(self.style.SUCCESS(f'Deleted file: {file_path}'))
                else:
                    self.stdout.write(self.style.WARNING(f'File not found: {file_path}'))

                # Delete the database entry
                
                self.stdout.write(self.style.SUCCESS(f'Deleted database entry for video {video.id}'))
                video.delete()
            except Exception as e:
                self.stderr.write(self.style.ERROR(f'Failed to delete file or database entry for video {video.id}: {str(e)}'))

        # Optionally, reset primary key sequence for SQLite
        with connection.cursor() as cursor:
            cursor.execute(f"DELETE FROM sqlite_sequence WHERE name='{Video._meta.db_table}';")
        self.stdout.write(self.style.SUCCESS('Reset primary key sequence for Video model'))



