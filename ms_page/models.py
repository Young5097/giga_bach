from django.db import models


class UploadAudio(models.Model):
    audio_file = models.FileField(upload_to="media/input_audio/")
