from django.urls import path
from . import views
<<<<<<< HEAD
from .views import board, create_post, post_detail, edit_post, delete_post
=======
from .views import board, create_post, delete_post
>>>>>>> eeb6e9f7fb30e90dea0759d077c4b75b2f9bc960

urlpatterns = [
    path("board/", board, name="board"),
    path("create_post/", create_post, name="create_post"),
<<<<<<< HEAD
    path('post/<int:post_id>/', post_detail, name='post_detail'),
    path('edit_post/<int:post_id>/', edit_post, name='edit_post'),
    path('delete_post/<int:post_id>/', delete_post, name='delete_post'),


=======
    path("delete_post/<int:post_id>/", delete_post, name="delete_post"),
>>>>>>> eeb6e9f7fb30e90dea0759d077c4b75b2f9bc960
]
