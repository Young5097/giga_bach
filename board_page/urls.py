from django.urls import path
from . import views
from .views import board

urlpatterns = [
    path("board/", board, name="board"),
]
