from django.db import models

# Create your models here.

class Video(models.Model):
    title = models.CharField(max_length=70)
    description = models.TextField(max_length=200)
    video_file = models.FileField(upload_to='videos/')
    upload_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
