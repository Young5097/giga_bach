from django.db import models
from django.contrib.auth.models import User


class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="main_page_posts"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
