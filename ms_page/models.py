from django.db import models
from django.contrib.auth.models import User

class Song(models.Model):
    title = models.CharField(max_length=100)
    condition_track = models.CharField(max_length=100, null=True)
    content_track = models.CharField(max_length=100, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='songs')
    audio_file = models.FileField(upload_to="media/sound2midi")