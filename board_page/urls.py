from django.urls import path
from . import views
from .views import board, create_post

urlpatterns = [
    path("board/", board, name="board"),
    path("create_post/", create_post, name="create_post"),
]
