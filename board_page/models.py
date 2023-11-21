from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    audio_file = models.FileField(upload_to="media/board_audio", null=True, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["-created_at"]  # 최신 순으로 정렬
