from django.urls import path
from . import views
from .views import board, create_post, delete_post

urlpatterns = [
    path("board/", board, name="board"),
    path("create_post/", create_post, name="create_post"),
    path("delete_post/<int:post_id>/", delete_post, name="delete_post"),
]
