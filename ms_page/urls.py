from django.urls import path
from . import views
from .views import make_song

urlpatterns = [
    path("make_song/", make_song, name="make_song"),
]
