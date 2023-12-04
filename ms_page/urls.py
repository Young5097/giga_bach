from django.urls import path
from . import views
from .views import make_song, ms_result, download_midi

urlpatterns = [
    path("make_song/", make_song, name="make_song"),
    path('ms_result/', ms_result, name='ms_result'),
    path('download_midi/', download_midi, name='download_midi'),
]