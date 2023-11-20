from django import forms
from .models import Post  # Post 모델을 사용한다고 가정


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["title", "content"]
