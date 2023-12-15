from django.db import models

class Song(models.Model):
    title = models.CharField(max_length=100)
    audio_file = models.FileField(upload_to='sound2midi')